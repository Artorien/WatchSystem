document.addEventListener('DOMContentLoaded', () => {
  const tableBody = document.querySelector('#hashtagTable tbody');
  if (!tableBody) return;

  function loadHashtags() {
    fetch('http://localhost:3000/hashtags')
      .then(res => res.json())
      .then(data => {
        tableBody.innerHTML = '';
        data.forEach(row => {
          const tr = document.createElement('tr');
          tr.innerHTML = `
            <td>${row.id}</td>
            <td class="tagCell">${row.hashtag}</td>
            <td>
              <button class="editTagBtn editBtn"><i class="fas fa-edit"></i> Edit</button>
              <button class="deleteTagBtn deleteBtn"><i class="fas fa-trash"></i> Delete</button>
            </td>
          `;

          tr.querySelector('.deleteTagBtn').addEventListener('click', () => {
            fetch(`http://localhost:3000/hashtags/${row.id}`, { method: 'DELETE' })
              .then(() => tr.remove())
              .catch(err => console.error('Delete failed:', err));
          });

          tr.querySelector('.editTagBtn').addEventListener('click', () => {
            const tagCell = tr.querySelector('.tagCell');
            const oldTag = tagCell.textContent;
            const newTag = prompt('Edit Hashtag:', oldTag);

            if (newTag && newTag !== oldTag) {
              fetch(`http://localhost:3000/hashtags/${row.id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ tag: newTag })
              })
              .then(() => tagCell.textContent = newTag)
              .catch(err => console.error('Edit failed:', err));
            }
          });

          tableBody.appendChild(tr);
        });
      })
      .catch(err => console.error('Failed to load hashtags:', err));
  }

  loadHashtags();
});
