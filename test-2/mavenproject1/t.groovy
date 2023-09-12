//def fileContent = sh(script: "cat s2.txt", returnStdout: true)
def file = new File("s4.txt")
def scoreValue = null
def isAfterRating = false

if (file.exists()) {
    def text = file.text

    // Define the regular expression pattern to match the 'score' attribute after 'rating'
    def pattern = /rating="[^"]*"\s+score="(\d+)"/

    // Find all matches using the pattern
    def matcher = (text =~ pattern)

    // Initialize the 'scoreValue' to null
    scoreValue = null

    // Iterate through the matches and consider only 'score' key after 'rating' keyword
    matcher.each { match ->
        // Extract the matched text
        def matchText = match[0]

        // Extract the 'score' value from the match
        scoreValue = match[1].toInteger()

        // Check if 'rating' is found, and set 'isAfterRating' flag
        if (matchText.contains('rating')) {
            isAfterRating = true
        }
    }
} else {
    println "File 's2.txt' not found."
}

// Check if 'rating' and 'score' are found, and print the result
if (isAfterRating && scoreValue != null) {
    if (scoreValue >= 80) {
        println "Correct - Score: $scoreValue"
    } else {
        println "Incorrect - Score: $scoreValue"
    }
} else {
    println "Rating and Score value not found after 'rating' to determine correctness."
}

// Return 0 as the exit status
return 0

