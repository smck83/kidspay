# Minimal static host for Kids Pay
FROM nginx:alpine
COPY index.html manifest.webmanifest sw.js *.png /usr/share/nginx/html/
EXPOSE 80
