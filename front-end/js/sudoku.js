    async function loadGrid() {
      try {
        const response = await fetch('http://127.0.0.1:8000/newgrid?gridId=mock1');
        if (!response.ok) throw new Error('Network response was not ok');

        const data = await response.json();
        const grid = data.grid;
        console.log(data)
        console.log(grid.length)
        const container = document.getElementById('grid-container');
        // console.log(data)
        
        
        container.innerHTML = ''; // clear old content

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
          container.appendChild(tr);
        }

      } catch (error) {
        console.error('Error fetching grid:', error);
      }
    }

    // Call on page load
    window.onload = loadGrid;