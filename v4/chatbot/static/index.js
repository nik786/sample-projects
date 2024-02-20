// console.log("hi");
class chatbot {
  constructor() {
    this.options = ["Vinz", "Eureka"];
    this.questions = [
      "hi",
      "how are you",
      "Vinz",
      "Eureka",
      "What is Amazon Inspector?",
      "What are the key benefits of Amazon Inspector?",
    ];
    this.answers = [
      "hello",
      "fine",
      "It is gateway service that provides dynamic routing, monitoring, resiliency, security, and more",
      "REST-based server that is used for load balancing and failover of middle-tier services",
      "Amazon Inspector is an automated vulnerability management service that continually scans Amazon Elastic Compute Cloud (EC2), AWS Lambda functions, andcontainer workloads for software vulnerabilities and unintended network exposure",
    ];
    this.assistant_name = "Plato";
    this.assistant_description = "Your personal asssistant";
    this.input_placeholder = "Write your query...";
    this.reply_time = 1; // in seconds

    // elements are here
    this.assistant_name_ele = document.getElementById("assistant_name");
    this.assistant_description_ele = document.getElementById(
      "assistant_description"
    );
    this.options_ele = document.getElementById("options");
    this.chat_ele = document.getElementById("chat");
    this.input_ele = document.getElementById("input");
    this.chatbot_ele = document.getElementById("chatbot");
    this.chat_circle_ele = document.getElementById("chat_circle");
    this.cross = document.getElementById("cross");
    this.msg_audio = document.getElementById("msg_audio");
    this.msg_audio_s = document.getElementById("msg_audio_s");
    this.send_ele = document.getElementById("send");

    // fetch("../static/options.txt")
    //   .then((response) => {
    //     return response.text();
    //   })
    //   .then((data) => {
    //     this.options = data.split("\r\n");

    //     fetch("../static/questions.txt")
    //       .then((response) => {
    //         return response.text();
    //       })
    //       .then((text) => {
    //         this.questions = text.split("\r\n");

    //         fetch("../static/answers.txt")
    //           .then((res) => {
    //             return res.text();
    //           })
    //           .then((text) => {
    //             this.answers = text.split("\r\n");
    //             this.setThings();
    //           });
    //       });
    //   });

    this.options = Object.keys(options);
    this.questions = Object.keys(qa);
    this.answers = Object.values(qa);

    for (let i = 0; i < Object.keys(options).length; i++) {
      this.questions.push(Object.keys(options)[i]);
      this.answers.push(Object.values(options)[i]);
    }

    console.log(this.questions);
    console.log(this.answers);
    this.setThings();
  }

  setThings = () => {
    this.assistant_name_ele.innerHTML += this.assistant_name;
    this.assistant_description_ele.innerText = this.assistant_description;
    for (let i = 0; i < this.options.length; i++) {
      this.options_ele.innerHTML +=
        `<div onclick='cb.option_send(this)'>` + this.options[i] + `</div>`;
    }
    this.input_ele.placeholder = this.input_placeholder;

    //putting the functions together
    this.chat_circle_ele.onclick = this.open;
    this.cross.onclick = this.close;
    this.send_ele.onclick = this.send;
    // this.input_ele.addEventListener("keydown", function (event) {
    //   if (event.key === "Enter") {
    //     this.send();
    //   }
    // });

    this.input_ele.onkeydown = (event) => {
      if (event.key === "Enter") {
        this.send();
      }
    };
  };

  sendMessage(message) {
    const userInput = document.getElementById("input").value;

    document.getElementById("input").value = "";

    // fetch("/get_response", {
    //   method: "POST",
    //   headers: {
    //     "Content-Type": "application/x-www-form-urlencoded",
    //   },
    //   body: `user_input=${message}`,
    // })
    //   .then((response) => response.json())

    //   .then((data) => {
    //     console.log(data);
    //     this.chat_ele.innerHTML += this.return_chatbot_msg(data.response);
    //   });

    this.get(message);
  }

  close = () => {
    this.chatbot_ele.style.display = "none";
    this.chat_circle_ele.style.display = "flex";
  };

  open = () => {
    this.chat_circle_ele.style.display = "none";
    this.chatbot_ele.style.display = "flex";
  };

  return_user_msg = (msg) => {
    return (
      `<div class="full_right">
<div class="small_right">
<div>` +
      msg +
      `</div>
</div>
</div>`
    );
  };

  return_chatbot_msg = (msg) => {
    return (
      `<div class="full">
      <img src="../static/bot.png" alt="" class="bot_img" />
<div class="small">
<div>` +
      msg +
      `</div>
</div>
</div>`
    );
  };

  scroll_up = () => {
    this.chat_ele.scrollTo(0, 500);
  };

  send = () => {
    // this.msg_audio_s.play();
    this.chat_ele.innerHTML += this.return_user_msg(this.input_ele.value);
    //    this.get(this.input_ele.value);
    this.sendMessage(this.input_ele.value);
    this.input_ele.value = "";
    this.scroll_up();
  };

  get = (msg) => {
    setTimeout(() => {
      // this.msg_audio.play();
      this.confidence = [];

      let user = msg;
      for (let i = 0; i < this.questions.length; i++) {
        this.confidence.push(0);
        let indi_questions_split = this.questions[i].split(" ");
        let user_split = user.split(" ");
        // console.log(msg);
        for (let j = 0; j <= user_split.length; j++) {
          if (indi_questions_split.includes(user_split[j])) {
            this.confidence[i] += 1;
          }
        }
      }

      // console.log(this.confidence);
      let percent_array = [];

      for (let i = 0; i < this.confidence.length; i++) {
        let user_split = user.split(" ");
        let percent = parseInt((this.confidence[i] / user_split.length) * 100);
        percent_array.push(percent);
      }

      // console.log(percent_array);

      let max = -1;
      for (let i = 0; i < percent_array.length; i++) {
        if (percent_array[i] > max && percent_array[i] > 30) {
          max = i;
        }
      }

      // console.log(max);
      if (max == -1) {
        this.chat_ele.innerHTML += this.return_chatbot_msg(
          "I am not able to understand you."
        );
      } else {
        this.chat_ele.innerHTML += this.return_chatbot_msg(this.answers[max]);
      }

      this.scroll_up();
    }, 1500);
  };

  option_send = (ele) => {
    // console.log(ele.innerText);
    this.msg_audio_s.play();
    // this.chat_ele.innerHTML += this.return_user_msg(ele.innerText);
    this.get(ele.innerText);
    this.input_ele.value = "";
    this.scroll_up();
  };
}
console.log("hello");
let all_faq_question = Object.keys(faq);
let all_faq_answers = Object.values(faq);
let all_deliver_questions = Object.keys(deliver);
let all_deliver_answers = Object.values(deliver);
let faq_indi_question = document.getElementsByClassName("faq_indi_question");
let faq_indi_answer = document.getElementsByClassName("faq_indi_answer");
let s2_1 = document.getElementsByClassName("s2_1");
// console.log(ul);
// console.log("ul--");
// ul[0].innerHTML = "";

for (let i = 0; i < all_deliver_questions.length; i++) {
  s2_1[0].innerHTML +=
    `<div class="faq_indi_2">
    <div class="question_svg">
      <svg
        viewBox="0 0 24 24"
        xmlns="http://www.w3.org/2000/svg"
        fill="red"
        height="24"
        width="24"
        onclick="plus2(` +
    i +
    `)"
      >
        <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
        <g
          id="SVGRepo_tracerCarrier"
          stroke-linecap="round"
          stroke-linejoin="round"
        ></g>
        <g id="SVGRepo_iconCarrier">
          <title></title>
          <g id="Complete">
            <g id="add-square">
              <g>
                <rect
                  data-name="--Rectangle"
                  fill="none"
                  height="20"
                  id="_--Rectangle"
                  rx="2"
                  ry="2"
                  stroke="red"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  width="20"
                  x="2"
                  y="2"
                ></rect>
                <line
                  fill="none"
                  stroke="red"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  x1="15.5"
                  x2="8.5"
                  y1="12"
                  y2="12"
                ></line>
                <line
                  fill="none"
                  stroke="red"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  x1="12"
                  x2="12"
                  y1="15.5"
                  y2="8.5"
                ></line>
              </g>
            </g>
          </g>
        </g>
      </svg>
      <div class="faq_indi_question2">` +
    all_deliver_questions[i] +
    `</div>
    </div>
    <div class="faq_indi_answer2">
      ` +
    all_deliver_answers[i] +
    `
    </div>
  </div>`;
}

for (let i = 0; i < faq_indi_question.length; i++) {
  faq_indi_question[i].innerText = all_faq_question[i];
}
for (let i = 0; i < faq_indi_answer.length; i++) {
  faq_indi_answer[i].innerText = all_faq_answers[i];
}

function plus(num) {
  let n = document.getElementsByClassName("faq_indi_answer");
  for (let i = 0; i < n.length; i++) {
    n[i].style.display = "none";
  }
  document.getElementsByClassName("faq_indi_answer")[num - 1].style.display =
    "block";
}
function plus2(num) {
  let n = document.getElementsByClassName("faq_indi_answer2");
  for (let i = 0; i < n.length; i++) {
    n[i].style.display = "none";
  }
  document.getElementsByClassName("faq_indi_answer2")[num].style.display =
    "block";
}

function dpop() {
  document.getElementsByClassName("popup")[0].style.display = "none";
}

let cb = new chatbot();
