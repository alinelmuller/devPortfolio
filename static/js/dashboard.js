document.addEventListener("DOMContentLoaded", () => {
    const forms = document.querySelectorAll("form");
    forms.forEach(form => {
        form.addEventListener("submit", async (e) => {
            e.preventDefault();
            const formData = new FormData(form);
            const response = await fetch(form.action, {
                method: "POST",
                body: formData,
                headers: {
                    "X-CSRFToken": form.querySelector("[name=csrfmiddlewaretoken]").value
                }
            });
            if (response.ok) {
                alert("Changes saved successfully!");
                location.reload(); // Refresh to update UI
            } else {
                alert("Error saving changes. Please try again.");
            }
        });
    });

    // Add Delete functionality for skills
    document.querySelectorAll(".delete-skill").forEach(button => {
        button.addEventListener("click", async (e) => {
            const skillId = e.target.closest(".skill").dataset.skillId;
            const response = await fetch(`/delete-skill/${skillId}/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value
                }
            });
            if (response.ok) {
                e.target.closest(".skill").remove();
            } else {
                alert("Failed to delete skill. Please try again.");
            }
        });
    });
});
