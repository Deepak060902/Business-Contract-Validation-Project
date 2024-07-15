function updateFileName(inputId) {
  const inputElement = document.getElementById(inputId);
  const labelElement = document.getElementById(inputId + 'Label');
  if (inputElement.files.length > 0) {
    labelElement.textContent = inputElement.files[0].name;
  } else {
    labelElement.textContent = `Choose ${inputId === 'contractFile' ? 'First' : 'Second'} PDF`;
  }
}

function viewPdf() {
  if (pdfUrl) {
    window.open(pdfUrl, '_blank');
  }
}

function downloadPdf() {
  if (pdfUrl) {
    const a = document.createElement('a');
    a.href = pdfUrl;
    a.download = 'merged_document.pdf';
    a.click();
  }
}


let pdfUrl = "";
let summary = "";

document.getElementById('uploadForm').addEventListener('submit', async function (e) {
  e.preventDefault();
  
  const contractFileInput = document.getElementById('contractFile');
  const templateFileInput = document.getElementById('templateFile');
  const contractFile = contractFileInput.files[0];
  const templateFile = templateFileInput.files[0];
  const formData = new FormData();
  formData.append('file', contractFile);
  formData.append('file1', templateFile);

  if (!contractFile || !templateFile) {
    alert('Please select both PDF files.');
    return;
  }

  try {
    const response = await fetch('/api/upload', {
      method: 'POST',
      body: formData,
    });
    if (response.ok) {
      const result = await response.json();
      const pdfBlob = base64ToBlob(result.pdf, 'application/pdf');
      pdfUrl = URL.createObjectURL(pdfBlob);
      summary = result.summary;
      
      console.log(summary)

      document.getElementById('mergedPdfName').textContent = 'highlighted_contract.pdf';
      document.getElementById('output').classList.remove('hidden');

      const summaryContainer = document.getElementById('summaryContainer');
      const summaryText = document.getElementById('summaryText');


      
      summaryText.innerHTML = summary;
      summaryContainer.classList.remove('hidden');

      const loadingTask = pdfjsLib.getDocument(pdfUrl);
      loadingTask.promise.then(pdf => {
        console.log('PDF loaded');
        
        const pdfContainer = document.getElementById('pdfContainer');
        pdfContainer.innerHTML = ''; // Clear any existing content
        
        document.getElementById('responseBox').style.display = 'block';
        // Loop through all the pages
        for (let pageNumber = 1; pageNumber <= pdf.numPages; pageNumber++) {
          pdf.getPage(pageNumber).then(page => {
            console.log('Page ' + pageNumber + ' loaded');
            
            const scale = 1.5;
            const viewport = page.getViewport({ scale: scale });
            
            // Create a canvas element for each page
            const canvas = document.createElement('canvas');
            canvas.classList.add('pdf-page');
            canvas.className = 'container p-6 border border-slate-600'
            const context = canvas.getContext('2d');
            canvas.height = viewport.height;
            canvas.width = viewport.width;
            pdfContainer.appendChild(canvas);
            
            // Render PDF page into canvas context
            const renderContext = {
              canvasContext: context,
              viewport: viewport
            };
            const renderTask = page.render(renderContext);
            renderTask.promise.then(() => {
              console.log('Page ' + pageNumber + ' rendered');
            });
          });
        }
      }, reason => {
        console.error('Error loading PDF: ' + reason);
      });
    } else {
      const errorResult = await response.json();
      document.getElementById('responseMessage').textContent = 'Failed to process the file: ' + errorResult.detail;
    }
  } catch (error) {
    document.getElementById('responseMessage').textContent = 'Error uploading file.';
    console.error('Error:', error);
  }
});

function base64ToBlob(base64, mimeType) {
  const byteCharacters = atob(base64);
  const byteNumbers = new Array(byteCharacters.length);
  for (let i = 0; i < byteCharacters.length; i++) {
    byteNumbers[i] = byteCharacters.charCodeAt(i);
  }
  const byteArray = new Uint8Array(byteNumbers);
  return new Blob([byteArray], { type: mimeType });
}