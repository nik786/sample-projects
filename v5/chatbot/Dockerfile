# Use CentOS as the base image
FROM centos/httpd

# Set maintainer label


# Install additional packages (git, vim, curl, net-tools)
RUN yum install -y git vim curl net-tools && \
    yum clean all

# Copy/mount HTML files into the container
ADD chat.tar.gz /var/www/html/

# Set ownership and permissions for Apache
RUN chown -R apache:apache /var/www/html/ && \
    chmod 755 /var/www/html/*

# Expose port 80
EXPOSE 80

# Set the default command to start Apache HTTP Server
CMD ["/usr/sbin/httpd", "-D", "FOREGROUND"]
