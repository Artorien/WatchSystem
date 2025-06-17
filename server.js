const express = require('express');
const cors = require('cors');
const { Pool } = require('pg');

const app = express();
const port = 3000;

app.use(cors());
app.use(express.json());


const pool = new Pool({
  user: 'postgres',
  host: 'localhost',
  database: 'postgres',
  password: 'WatchHumans!',
  port: 5432,
});


app.get('/data', async (req, res) => {
  try {
    const result = await pool.query('SELECT * FROM flagged');
    res.json(result.rows);
  } catch (err) {
    console.error(err);
    res.status(500).send('Database query error');
  }
});

app.post('/move', async (req, res) => {
  const { id } = req.body;

  try {
    //Get the row from flagged
    const result = await pool.query('SELECT * FROM flagged WHERE id = $1', [id]);
    const row = result.rows[0];

    if (!row) {
      return res.status(404).json({ error: 'Row not found' });
    }

    //Insert into not_flagged
    await pool.query(
    'INSERT INTO not_flagged (hashtag, content, time_stamp, played) VALUES ($1, $2, $3, $4)',
    [row.hashtag, row.content, row.time_stamp, false]
    );


    //Delete from flagged
    await pool.query('DELETE FROM flagged WHERE id = $1', [id]);

    res.json({ success: true });
  } catch (err) {
    console.error('Move failed:', err);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

app.delete('/delete/:id', async (req, res) => {
  const { id } = req.params;

  try {
    await pool.query('DELETE FROM flagged WHERE id = $1', [id]);
    res.json({ success: true });
  } catch (err) {
    console.error('Delete failed:', err);
    res.status(500).json({ error: 'Delete error' });
  }
});

app.put('/edit/:id', async (req, res) => {
  const { id } = req.params;
  const { content } = req.body;

  try {
    await pool.query('UPDATE flagged SET content = $1 WHERE id = $2', [content, id]);
    res.json({ success: true });
  } catch (err) {
    console.error('Edit failed:', err);
    res.status(500).json({ error: 'Edit error' });
  }
});



app.listen(port, () => {
  console.log(`Server listening at http://localhost:${port}`);
});