document.addEventListener('DOMContentLoaded', () => {
  const tableBody  = document.querySelector('#captionsTable tbody');
  const searchBtn  = document.getElementById('searchBtn');
  const searchInput= document.getElementById('searchInput');
  const sortSelect = document.getElementById('sortOrder');

  if (!tableBody || !searchBtn || !searchInput || !sortSelect) return;

  function loadTable(filterTag = '', sortOrder = 'desc') {
    fetch('http://localhost:3000/captions')
      .then(res => res.json())
      .then(data => {
        let rows = data;
        if (filterTag) {
          const ft = filterTag.toLowerCase();
          rows = rows.filter(r => r.hashtag.toLowerCase().includes(ft));
        }
        rows.sort((a, b) => {
          const ta = new Date(a.time_stamp).getTime();
          const tb = new Date(b.time_stamp).getTime();
          return sortOrder === 'asc' ? ta - tb : tb - ta;
        });

        tableBody.innerHTML = '';
        rows.forEach(row => {
          const tr = document.createElement('tr');
          tr.innerHTML = `
            <td>${row.id}</td>
            <td>${row.hashtag}</td>
            <td class="editable">${row.content}</td>
            <td>${new Date(row.time_stamp).toLocaleString()}</td>
            <td>
              <button class="editBtn"><i class="fas fa-edit"></i> Edit</button>
              <button class="deleteBtn"><i class="fas fa-trash"></i> Delete</button>
            </td>
          `;

          tr.querySelector('.editBtn').addEventListener('click', () => {
            const contentTd = tr.querySelector('.editable');
            const oldVal = contentTd.textContent;
            const newVal = prompt('Edit caption:', oldVal);
            if (newVal && newVal !== oldVal) {
              fetch(`http://localhost:5000/captions/${row.id}`, {
                method: 'PUT',
                headers: {'Content-Type':'application/json'},
                body: JSON.stringify({ content: newVal })
              })
              .then(r => {
                if (!r.ok) throw new Error('Edit failed');
                contentTd.textContent = newVal;
              })
              .catch(() => alert('Failed to edit caption'));
            }
          });

          tr.querySelector('.deleteBtn').addEventListener('click', () => {
            if (!confirm('Delete this caption?')) return;
            fetch(`http://localhost:3000/captions/${row.id}`, { method: 'DELETE' })
              .then(r => {
                if (!r.ok) throw new Error('Delete failed');
                tr.remove();
              })
              .catch(() => alert('Failed to delete caption'));
          });

          tableBody.appendChild(tr);
        });
      })
      .catch(err => console.error('Failed to load captions:', err));
  }

  loadTable();

  searchBtn.addEventListener('click', () => {
    loadTable(searchInput.value.trim(), sortSelect.value);
  });
  sortSelect.addEventListener('change', () => {
    loadTable(searchInput.value.trim(), sortSelect.value);
  });
});
