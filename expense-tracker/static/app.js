const fileInput = document.getElementById('file-input');
const preview   = document.getElementById('preview');
const dropZone  = document.getElementById('drop-zone');

function showPreview(file) {
  if (!file) return;
  const reader = new FileReader();
  reader.onload = (e) => {
    preview.src = e.target.result;
    preview.classList.remove('hidden');
    dropZone.classList.add('has-preview');
  };
  reader.readAsDataURL(file);
}

fileInput.addEventListener('change', (e) => showPreview(e.target.files[0]));

dropZone.addEventListener('dragover', (e) => {
  e.preventDefault();
  dropZone.classList.add('drag-over');
});

dropZone.addEventListener('dragleave', () => dropZone.classList.remove('drag-over'));

dropZone.addEventListener('drop', (e) => {
  e.preventDefault();
  dropZone.classList.remove('drag-over');
  const file = e.dataTransfer.files[0];
  if (file) {
    const dt = new DataTransfer();
    dt.items.add(file);
    fileInput.files = dt.files;
    showPreview(file);
  }
});

document.body.addEventListener('htmx:afterSwap', (e) => {
  if (e.detail.target.id === 'result') {
    document.getElementById('result-panel').scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
});
