document.addEventListener("DOMContentLoaded", function () {
  // const textElement = document.getElementById("typing-text");
  // const text = textElement.textContent;
  // textElement.textContent = "";
  // let index = 0;

  // function type() {
  //   if (index < text.length) {
  //     textElement.textContent += text.charAt(index);
  //     index++;
  //     setTimeout(type, 100); // Adjust the speed of typing here (in milliseconds)
  //   } else {
  //     setTimeout(() => {
  //       textElement.textContent = "";
  //       index = 0;
  //       setTimeout(type, 2000); // Pause for 2 seconds before restarting
  //     }, 2000); // Pause for 2 seconds after finishing typing
  //   }
  // }

  // type();
});

document.getElementById("pdfFile").addEventListener("change", function (event) {
  const file = event.target.files[0];
  if (file && file.type === "application/pdf") {
    const fileURL = URL.createObjectURL(file);
    document.getElementById("pdfViewer").src = fileURL;
  } else {
    alert("Please upload a valid PDF file.");
  }
});


document.addEventListener('DOMContentLoaded', () => {
  const dragDropArea = document.getElementById('drag-drop-area');
  const fileInput = document.getElementById('pdfFile');
  const uploadButton = document.getElementById('uploadButton');
  const removeIcon = document.getElementById('remove-icon');
  let file;

  dragDropArea.addEventListener('dragover', (event) => {
    event.preventDefault();
    dragDropArea.classList.add('dragover');
  });

  dragDropArea.addEventListener('dragleave', () => {
    dragDropArea.classList.remove('dragover');
  });

  dragDropArea.addEventListener('drop', (event) => {
    event.preventDefault();
    dragDropArea.classList.remove('dragover');
    file = event.dataTransfer.files[0];
    if (file && file.type === "application/pdf") {
      const fileURL = URL.createObjectURL(file);
      document.getElementById("pdfViewer").src = fileURL;
    }
    fileInput.files = event.dataTransfer.files;
    dragDropArea.innerHTML = `<p>File: ${file.name}</p>`;
  });

  dragDropArea.addEventListener('click', () => {
    fileInput.click();
  });

  fileInput.addEventListener('change', () => {
    file = fileInput.files[0];
    dragDropArea.innerHTML = `<p>File: ${file.name}</p>`;
  });

  removeIcon.addEventListener('click', (event) => {
    event.stopPropagation();
    file = null;
    fileInput.value = '';
    dragDropArea.innerHTML = `<span class="remove-icon" id="remove-icon">&times;</span><p>Drag and drop a file here or click to select a file</p>`;
    document.getElementById('remove-icon').style.display = 'none';
  });


  uploadButton.addEventListener('click', () => {
    if (!file) {
      alert('Please select a file first.');
      return;
    }
    entities = $("#spacyentities").val();
    if (entities.length == 0) {
      alert("Please select entities you want to fetch from the doc");
      return;
    }
    $("#uploadForm").submit();
  });
});
$(document).ready(function () {
  $('#spacyentities').select2({
    closeOnSelect: false
  });
});
