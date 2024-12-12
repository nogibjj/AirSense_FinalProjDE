const databricksDot = document.getElementById("databricks-dot");
const rdsDot = document.getElementById("rds-dot");
const checkStatusButton = document.getElementById("check-status");
const updateTableButton = document.getElementById("update-table");
const serviceTransferTable = document.getElementById("service-transfer-table").getElementsByTagName("tbody")[0];

// Function to update the dot's color
function updateDot(dotElement, status) {
    if (status === "connected") {
        dotElement.style.backgroundColor = "green";
    } else if (status === "disconnected") {
        dotElement.style.backgroundColor = "red";
    } else {
        dotElement.style.backgroundColor = "gray";
    }
}

// Event listener for the "Check Status" button
checkStatusButton.addEventListener("click", async () => {
    // Check Databricks status
    try {
        const databricksResponse = await fetch("/dbstatus");
        const databricksResult = await databricksResponse.json();
        updateDot(databricksDot, databricksResult["Databricks is connected"] ? "connected" : "disconnected");
    } catch (error) {
        updateDot(databricksDot, "disconnected");
        console.error("Error checking Databricks status:", error);
    }

    // Check RDS status
    try {
        const rdsResponse = await fetch("/rdsstatus");
        const rdsResult = await rdsResponse.json();
        updateDot(rdsDot, rdsResult["RDS is connected"] ? "connected" : "disconnected");
    } catch (error) {
        updateDot(rdsDot, "disconnected");
        console.error("Error checking RDS status:", error);
    }
});

// Function to load the service transfer table
async function loadServiceTransferTable() {
    try {
        const response = await fetch("/service_transfer");
        const result = await response.json();

        // Clear existing rows
        serviceTransferTable.innerHTML = "";

        if (result.data.length === 0) {
            serviceTransferTable.innerHTML = `<tr><td colspan="4">No data available.</td></tr>`;
            return;
        }

        // Populate table with data
        result.data.forEach(row => {
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td>${row.id}</td>
                <td>${row.tablename}</td>
                <td>${row.last_transfer_date}</td>
                <td>${row.transfer_count}</td>
            `;
            serviceTransferTable.appendChild(tr);
        });
    } catch (error) {
        console.error("Error loading service transfer table:", error);
    }
}

// Event listener for the "Update Table" button
updateTableButton.addEventListener("click", loadServiceTransferTable);

// Load the table on page load
loadServiceTransferTable();
