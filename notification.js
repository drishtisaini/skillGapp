document.querySelectorAll(".mark-read").forEach(button => {
  button.addEventListener("click", function() {
    const notification = this.parentElement;
    notification.classList.remove("unread");
    this.remove(); // remove button after marking read
  });
});
