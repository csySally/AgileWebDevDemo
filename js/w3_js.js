function wordle(target, guess) {
  target = "peach";
  guess = document.getElementById("guess").value;
  if (guess.length != target.length) {
    document.getElementById("result").innerHTML =
      "Please enter a word with 5 letters.";
    return;
  }
  let result = "";
  for (let i = 0; i < target.length; i++) {
    if (target.charAt(i) == guess.charAt(i)) {
      result += `The ${i + 1} letter is in the correct position. `;
    } else if (target.indexOf(guess.charAt(i)) < 0) {
      result += `The ${i + 1} letter is not in the word. `;
    } else {
      result += `The ${
        i + 1
      } letter is in the word, but not in the correct position. `;
    }
  }
  document.getElementById("result").innerHTML = result;
}
