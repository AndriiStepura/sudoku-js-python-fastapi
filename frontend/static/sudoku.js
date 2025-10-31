const host = "http://localhost:8000" // Dokerized host
// For local debug
// const host = "http://127.0.0.1:8000"

const apiVersion = "v1"

async function loadGrid(gridId = "mock1") {
  try {
    document.getElementById("gridId").value = gridId;
    console.log("gridId in loadGrid is " + gridId);

    getEndPoint = host + "/" + apiVersion + "/newgrid?gridId=" + gridId;
    const response = await fetch(getEndPoint);
    if (!response.ok) throw new Error("Network response was not ok");
    const data = await response.json();
    const grid = data.grid;
    // console.log(data)
    // console.log(grid.length)
    const boardContainer = document.getElementById("grid-container");

    boardContainer.innerHTML = ""; // clear old content

    const rowSize = 9; // TODO read from config later to have feature build custom game boards
    for (let i = 0; i < grid.length; i += rowSize) {
      const tr = document.createElement("tr");
      for (let j = 0; j < rowSize && i + j < grid.length; j++) {
        const cell = grid[i + j];
        const td = document.createElement("td");
        const input = document.createElement("input");

        input.type = "text";
        input.id = `cell-${i + j}`;
        input.value = cell.value === null ? "" : cell.value;
        if (!cell.changeable) input.disabled = true;

        td.appendChild(input);
        tr.appendChild(td);
      }
      boardContainer.appendChild(tr);
    }
  } catch (error) {
    console.log("error is " + error);
    console.error("Error fetching grid:", error);
  }
}

function collectGridValues() {
  const inputs = document.querySelectorAll('input[id^="cell-"]');
  const values = Array.from(inputs).map((inp) => {
    const v = inp.value.trim();
    return v === "" ? 0 : parseInt(v, 10);
  });

  // Convert array to 9x9 grid, TODO size from settings later
  const grid = [];
  for (let i = 0; i < values.length; i += 9) {
    grid.push(values.slice(i, i + 9));
  }

  return grid;
}

async function verifySudoku() {
  // console.log("Hi from verifySudoku")
  gridId = checkGridId();
  console.log("gridIdIn is " + gridId);

  const grid = collectGridValues();
  // console.log(grid)
  const payload = {
    gridId: gridId,
    grid: grid,
  };

  try {
    const response = await fetch(host + "/" + apiVersion + "/verifygrid/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!response.ok) throw new Error("Failed to send grid");
    const result = await response.json();
    console.log("Server response:", result);
    // Propagate verification errors to UI
    showCriticalErrors(result.errorsMessages);
    showValidationErrors(result.errorCells);
  } catch (error) {
    console.error("Error sending grid:", error);
    showCriticalErrors(error);
  }
}

function showCriticalErrors(errors) {
  let success = false;
  const criticalErrorsContainer = document.getElementById("criticalErrors");
  criticalErrorsContainer.innerHTML = ""; // clear old content

  if (!errors || errors.length === 0) {
    // if no errors - looks like your resolved this sudoku
    success = true;
    errors.push("CONGRATULATIONS SUDOKU RESOLVED");
  }

  // Create heading
  const title = document.createElement("h2");
  title.textContent = "Critical errors";
  criticalErrorsContainer.appendChild(title);

  // Create list
  const ul = document.createElement("ul");

  // Put list of errors
  errors.forEach((err) => {
    const li = document.createElement("li");
    const mark = document.createElement("mark");
    const kbd = document.createElement("kbd");
    if (success) {
      kbd.style.cssText = "background-color: green;";
    }

    kbd.textContent = err;

    mark.appendChild(kbd);
    li.appendChild(mark);
    ul.appendChild(li);
  });

  criticalErrorsContainer.appendChild(ul);
}

function showValidationErrors(errors) {
  const validationErrorsContainer = document.getElementById("validationErrors");
  validationErrorsContainer.innerHTML = ""; // clear old content

  if (!errors || errors.length === 0) {
    return; // nothing to show
  }

  // Create heading
  const title = document.createElement("h3");
  title.textContent = "Validation errors";
  validationErrorsContainer.appendChild(title);

  // Create list
  const ul = document.createElement("ul");

  // Put list of errors
  errors.forEach((err) => {
    const li = document.createElement("li");
    const mark = document.createElement("mark");
    mark.textContent =
      "x:" +
      err.x +
      "y:" +
      err.y +
      " errors - " +
      err.cellErrorsMessages.toString();
    li.appendChild(mark);
    ul.appendChild(li);
  });

  validationErrorsContainer.appendChild(ul);
}

function checkGridId() {
  console.log("on load " + document.getElementById("gridId").value);
  // use this input field as temp storage for gridId value, alternatively - localStorage option
  return document.getElementById("gridId").value;
}

function populateGrid(gridId) {
  if (gridId == "mock1") {
    // mock1_resolved_as_array
    gridArray = [
      [5, 3, 4, 6, 7, 8, 9, 1, 2],
      [6, 7, 2, 1, 9, 5, 3, 4, 8],
      [1, 9, 8, 3, 4, 2, 5, 6, 7],
      [8, 5, 9, 7, 6, 1, 4, 2, 3],
      [4, 2, 6, 8, 5, 3, 7, 9, 1],
      [7, 1, 3, 9, 2, 4, 8, 5, 6],
      [9, 6, 1, 5, 3, 7, 2, 8, 4],
      [2, 8, 7, 4, 1, 9, 6, 3, 5],
      [3, 4, 5, 2, 8, 6, 1, 7, 9],
    ];
  }

  if (!Array.isArray(gridArray) || gridArray.length === 0) {
    console.error("Invalid grid array");
    return;
  }

  let index = 0;
  for (let row = 0; row < gridArray.length; row++) {
    for (let col = 0; col < gridArray[row].length; col++) {
      const value = gridArray[row][col];
      const input = document.getElementById(`cell-${index}`);

      if (input) {
        input.value = value === 0 || value === null ? "" : value;
      }

      index++;
    }
  }
}

// Call on page load
window.onload = loadGrid();
