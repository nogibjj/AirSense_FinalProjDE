const databricksDot = document.getElementById("databricks-dot");
const rdsDot = document.getElementById("rds-dot");
const checkStatusButton = document.getElementById("check-status");
const updateTableButton = document.getElementById("update-table");
const transferForm = document.getElementById("transfer-form");
const transferStatus = document.getElementById("transfer-status");
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

// Check DB statuses
checkStatusButton.addEventListener("click", async () => {
    try {
        const databricksResponse = await fetch("/dbstatus");
        const databricksResult = await databricksResponse.json();
        updateDot(databricksDot, databricksResult["Databricks is connected"] ? "connected" : "disconnected");
    } catch (error) {
        updateDot(databricksDot, "disconnected");
        console.error("Error checking Databricks status:", error);
    }

    try {
        const rdsResponse = await fetch("/rdsstatus");
        const rdsResult = await rdsResponse.json();
        updateDot(rdsDot, rdsResult["RDS is connected"] ? "connected" : "disconnected");
    } catch (error) {
        updateDot(rdsDot, "disconnected");
        console.error("Error checking RDS status:", error);
    }
});

// Load service transfer table
updateTableButton.addEventListener("click", async () => {
    try {
        const response = await fetch("/service_transfer");
        const result = await response.json();

        serviceTransferTable.innerHTML = "";

        if (result.data.length === 0) {
            serviceTransferTable.innerHTML = `<tr><td colspan="4">No data available.</td></tr>`;
            return;
        }

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
});

// Transfer table from Databricks to RDS
transferForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const tableName = document.getElementById("table-name").value;

    transferStatus.innerHTML = `<strong>Status:</strong> Initiating transfer for table <em>${tableName}</em>...`;

    try {
        const response = await fetch("/transfer_table", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ table_name: tableName }),
        });

        const result = await response.json();

        if (response.ok) {
            transferStatus.innerHTML = `<strong>Status:</strong> Transfer successful!<br>
                Table Name: ${result.table_name}<br>
                Rows Transferred: ${result.rows_transferred}`;
        } else {
            transferStatus.innerHTML = `<strong>Status:</strong> Transfer failed. ${result.detail}`;
        }
    } catch (error) {
        transferStatus.innerHTML = `<strong>Status:</strong> Transfer failed. Error: ${error.message}`;
    }
});
