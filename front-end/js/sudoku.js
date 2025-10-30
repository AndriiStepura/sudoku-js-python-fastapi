async function loadGrid() {
  try {
    const response = await fetch('http://127.0.0.1:8000/newgrid?gridId=mock1');
    if (!response.ok) throw new Error('Network response was not ok');

    const data = await response.json();
    const grid = data.grid;
    console.log(data)
    console.log(grid.length)
    const boardContainer = document.getElementById('grid-container');
    // console.log(data)

    boardContainer.innerHTML = ''; // clear old content

    const rowSize = 9; // TODO read from config later to have feature build custom game boards
    for (let i = 0; i < grid.length; i += rowSize) {
      const tr = document.createElement('tr');
      for (let j = 0; j < rowSize && i + j < grid.length; j++) {
        const cell = grid[i + j];
        const td = document.createElement('td');
        const input = document.createElement('input');

        input.type = 'text';
        input.id = `cell-${i + j}`;
        input.value = cell.value === null ? '' : cell.value;
        if (!cell.changeable) input.disabled = true;

        td.appendChild(input);
        tr.appendChild(td);
      }
      boardContainer.appendChild(tr);
    }

  } catch (error) {
    console.error('Error fetching grid:', error);
  }
}


function collectGridValues() {
  const inputs = document.querySelectorAll('input[id^="cell-"]');
  const values = Array.from(inputs).map(inp => {
    const v = inp.value.trim();
    return v === '' ? 0 : parseInt(v, 10);
  });

  // Convert array to 9x9 grid, TODO size from settings later
  const grid = [];
  for (let i = 0; i < values.length; i += 9) {
    grid.push(values.slice(i, i + 9));
  }

  return grid;
}

async function verifySudoku() {
  const grid = collectGridValues();
  const payload = {
    gridId: "mock1",
    grid: grid
  };

  try {
    const response = await fetch('http://127.0.0.1:8000/verifygrid/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (!response.ok) throw new Error('Failed to send grid');
      const result = await response.json();
      console.log('Server response:', result);
      // Propagate verification errors to UI
      showCriticalErrors(result.errorsMessages);
  } catch (error) {
    console.error('Error sending grid:', error);
    showCriticalErrors(error);
  }  
}

function showCriticalErrors(errors) {
  const criticalErrorsContainer = document.getElementById('criticalErrors');
  criticalErrorsContainer.innerHTML = ''; // clear old content

  if (!errors || errors.length === 0) {
    return; // nothing to show
  }

  // Create heading
  const title = document.createElement('h2');
  title.textContent = 'Critical errors';
  criticalErrorsContainer.appendChild(title);

  // Create list
  const ul = document.createElement('ul');

  // Put list of errors
  errors.forEach(err => {
    const li = document.createElement('li');
    const mark = document.createElement('mark');
    const kbd = document.createElement('kbd');
    kbd.textContent = err;

    mark.appendChild(kbd);
    li.appendChild(mark);
    ul.appendChild(li);
  });

  criticalErrorsContainer.appendChild(ul);
}

// Call on page load
window.onload = loadGrid;