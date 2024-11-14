# Use the official Nginx image from the Docker Hub
FROM nginx:stable-alpine

# Copy custom configuration file from the current directory
COPY ngnix.conf /etc/nginx/conf.d/default.conf

# Expose port 80 to the outside world
EXPOSE 80

# Start Nginx when the container launches
CMD ["nginx", "-g", "daemon off;"]