document.addEventListener('DOMContentLoaded', () => {
  const tableBody = document.querySelector('#dataTable tbody');
  if (!tableBody) return;

  fetch('http://localhost:3000/data')
    .then(res => res.json())
    .then(data => {
      tableBody.innerHTML = '';
      data.forEach(row => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td>${row.id}</td>
          <td>${row.hashtag}</td>
          <td class="editable">${row.content}</td>
          <td>
            <button class="moveBtn"><i class="fas fa-arrows-alt"></i> Move</button>
            <button class="editTagBtn editBtn"><i class="fas fa-edit"></i> Edit</button>
            <button class="deleteTagBtn deleteBtn"><i class="fas fa-trash"></i> Delete</button>
          </td>
        `;

        tr.querySelector('.moveBtn').addEventListener('click', () => {
          fetch('http://localhost:3000/move', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id: row.id })
          })
          .then(res => {
            if (!res.ok) throw new Error('Move failed');
            return res.json();
          })
          .then(() => tr.remove())
          .catch(() => alert('Move failed'));
        });

        tr.querySelector('.deleteBtn').addEventListener('click', () => {
          fetch(`http://localhost:3000/delete/${row.id}`, { method: 'DELETE' })
            .then(res => {
              if (!res.ok) throw new Error('Delete failed');
              tr.remove();
            })
            .catch(() => alert('Delete failed'));
        });

        tr.querySelector('.editBtn').addEventListener('click', () => {
          const contentTd = tr.querySelector('.editable');
          const oldContent = contentTd.textContent;
          const newContent = prompt('Edit content:', oldContent);

          if (newContent && newContent !== oldContent) {
            fetch(`http://localhost:3000/edit/${row.id}`, {
              method: 'PUT',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ content: newContent })
            })
            .then(res => {
              if (!res.ok) throw new Error('Edit failed');
              contentTd.textContent = newContent;
            })
            .catch(() => alert('Edit failed'));
          }
        });

        tableBody.appendChild(tr);
      });
    })
    .catch(err => console.error('Failed to fetch data:', err));
});
