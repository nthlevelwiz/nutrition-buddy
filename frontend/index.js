let state = [
    ["today, 5/29", 1200, "dinner", 300, "steak", 300, 20, 15],
    ["5/28", 900, "lunch", 600, "eggs", 300, 20, 15],
    ["5/28", 600, "lunch", 300, "eggs", 300, 20, 15],
    ["5/28", 300, "breakfast", 300, "eggs", 300, 20, 15],
    ["5/27", 600, "lunch", 300, "eggs", 300, 20, 15],
    ["5/27", 300, "breakfast", 300, "eggs", 300, 20, 15]
];

function updateTable() {
    const tableBody = document.getElementById('food-table').getElementsByTagName('tbody')[0];
    tableBody.innerHTML = "";

    let lastDay = null;
    let lastMeal = null;
    let displayedMealcals = false;
    let displayedDaycalories = false;
    state.forEach((row, index) => {
        const newRow = tableBody.insertRow();

        row.forEach((cell, cellIndex) => {
            const newCell = newRow.insertCell(cellIndex);

            newCell.innerText = cell;
            if (cellIndex === 0) { // Day column
                if (cell === lastDay) {
                    newCell.innerText = '';
                } else {
                    lastDay = cell;
                    displayedMealcals = false;
                    displayedDaycalories = false;
                }
            } else if (cellIndex === 1) { // Day's Calories column
                console.log(row[0])
                console.log(cell)
                if (displayedDaycalories) {
                    newCell.innerText = '';
                }else{
                    displayedDaycalories = true;
                }
            } else if (cellIndex === 2) { // Meal column
                if (cell === lastMeal && row[0] === lastDay) {
                    newCell.innerText = '';
                } else {
                    lastMeal = cell;
                    displayedMealcals = false;
                }
            } else if (cellIndex === 3) { // Meal's Calories column
                if (displayedMealcals) {
                    newCell.innerText = '';
                }else{                  
                    displayedMealcals = true;
                }
            }
        });

        const actionCell = newRow.insertCell(8);
        actionCell.innerHTML = `<span class="delete-btn" onclick="deleteRow(${index})">X</span>`;
    });
}

document.addEventListener('DOMContentLoaded', () => {
    updateTable();
});


function addRow() {
    const day = document.getElementById('day').value;
    const meal = document.getElementById('meal').value;
    const foodItem = document.getElementById('food-item').value;
    const calories = parseInt(document.getElementById('calories').value);
    const weight = parseInt(document.getElementById('weight').value);
    const caloriesWeight = parseInt(document.getElementById('calories-weight').value);

    const newRow = [
        day,
        calculateDaysCalories(day, calories),
        meal,
        calculateMealsCalories(day, meal, calories),
        foodItem,
        calories,
        weight,
        caloriesWeight
    ];

    state.unshift(newRow);
    updateTable();
}

function deleteRow(index) {
    state.splice(index, 1);
    updateTable();
}

function calculateDaysCalories(day, calories) {
    let totalCalories = calories;
    state.forEach(row => {
        if (row[0] === day) {
            totalCalories += row[5];
        }
    });
    return totalCalories;
}

function calculateMealsCalories(day, meal, calories) {
    let totalCalories = calories;
    state.forEach(row => {
        if (row[0] === day && row[2] === meal) {
            totalCalories += row[5];
        }
    });
    return totalCalories;
}

document.addEventListener('DOMContentLoaded', () => {
    updateTable();
});
