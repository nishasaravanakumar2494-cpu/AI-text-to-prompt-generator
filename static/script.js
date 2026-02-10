function makePrompt() {
  const input = document.getElementById("inputText").value;
  const output = document.getElementById("outputText");

  if (input.trim() === "") {
    output.value = "Please write something first";
    return;
  }

  output.value = "Please wait...";

  fetch("/generate", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ text: input }),
  })
    .then((response) => response.json())
    .then((data) => {
      output.value = data.prompt;
    })
    .catch((error) => {
      output.value = "Error occurred";
    });
}
