<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Smart Shopping List & Bill Generator</title>
    <style>
        /* Modern Dark Theme Styling */
        * {
            box-sizing: border-box;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
        }

        body {
            background-color: #0f172a;
            color: #f8fafc;
            padding: 20px;
            display: flex;
            justify-content: center;
        }

        .app-container {
            width: 100%;
            max-width: 480px;
            background-color: #0f172a;
        }

        /* Header */
        .header {
            margin-bottom: 20px;
        }

        .header h1 {
            font-size: 22px;
            color: #ffffff;
        }

        .header .date-time {
            font-size: 13px;
            color: #3b82f6;
            font-weight: 600;
            margin-top: 4px;
        }

        /* Card Section */
        .card {
            background-color: #1e293b;
            border: 1px solid #334155;
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 16px;
        }

        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
        }

        .card-title {
            font-size: 14px;
            font-weight: bold;
            color: #3b82f6;
        }

        .btn-link {
            background: none;
            border: none;
            color: #f43f5e;
            font-weight: bold;
            cursor: pointer;
            font-size: 12px;
        }

        .btn-edit {
            color: #94a3b8;
        }

        /* Input Area */
        textarea {
            width: 100%;
            height: 90px;
            background-color: #020617;
            color: #ffffff;
            border: 1px solid #334155;
            border-radius: 8px;
            padding: 10px;
            font-size: 15px;
            resize: none;
            margin-bottom: 12px;
            outline: none;
        }

        /* Primary Action Button */
        .btn-primary {
            width: 100%;
            background-color: #3b82f6;
            color: white;
            border: none;
            padding: 12px;
            border-radius: 8px;
            font-weight: bold;
            font-size: 15px;
            cursor: pointer;
            transition: background 0.2s;
        }

        .btn-primary:hover {
            background-color: #2563eb;
        }

        .btn-success {
            background-color: #10b981;
        }

        .btn-success:hover {
            background-color: #059669;
        }

        /* Dynamic Item List */
        .item-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            background-color: #0f172a;
            padding: 10px 12px;
            border-radius: 8px;
            margin-bottom: 8px;
        }

        .item-left {
            display: flex;
            align-items: center;
            gap: 10px;
            flex: 1;
        }

        .item-left input[type="checkbox"] {
            width: 18px;
            height: 18px;
            accent-color: #10b981;
            cursor: pointer;
        }

        .item-left label {
            font-size: 15px;
            cursor: pointer;
            color: #f8fafc;
        }

        .price-container {
            display: flex;
            align-items: center;
            gap: 4px;
        }

        .price-container span {
            color: #94a3b8;
            font-size: 13px;
            font-weight: bold;
        }

        .price-input {
            width: 70px;
            background-color: #1e293b;
            border: 1px solid #334155;
            color: #10b981;
            font-weight: bold;
            text-align: center;
            padding: 6px;
            border-radius: 6px;
            font-size: 14px;
            outline: none;
        }

        /* Printable Receipt (Hidden by Default) */
        #printable-receipt {
            display: none;
            background: #ffffff;
            color: #0f172a;
            padding: 20px;
            border-radius: 8px;
            max-width: 400px;
            margin: 20px auto;
        }

        #printable-receipt h2 {
            text-align: center;
            font-size: 20px;
            text-transform: uppercase;
            border-bottom: 2px solid #e2e8f0;
            padding-bottom: 10px;
        }

        #printable-receipt .receipt-date {
            text-align: center;
            font-size: 12px;
            color: #64748b;
            margin: 8px 0 16px 0;
        }

        .receipt-table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 15px;
        }

        .receipt-table th, .receipt-table td {
            padding: 8px 0;
            text-align: left;
            border-bottom: 1px solid #e2e8f0;
            font-size: 14px;
        }

        .receipt-table th:last-child, .receipt-table td:last-child {
            text-align: right;
        }

        .receipt-total {
            display: flex;
            justify-content: space-between;
            font-weight: bold;
            font-size: 16px;
            border-top: 2px solid #0f172a;
            padding-top: 10px;
            color: #10b981;
        }

        /* Media Query for Browser Printing */
        @media print {
            body * {
                visibility: hidden;
            }
            #printable-receipt, #printable-receipt * {
                visibility: visible;
            }
            #printable-receipt {
                display: block !important;
                position: absolute;
                left: 0;
                top: 0;
                width: 100%;
            }
        }
    </style>
</head>
<body>

    <div class="app-container">
        <!-- App Header -->
        <div class="header">
            <h1>Smart Shopping List</h1>
            <div class="date-time" id="live-date-time">Loading date...</div>
        </div>

        <!-- Section 1: Input Box Card -->
        <div class="card" id="input-card">
            <div class="card-header">
                <span class="card-title">1. Write Items (Bengali / English)</span>
                <button class="btn-link" onclick="clearInput()">Clear</button>
            </div>
            <textarea id="text-input" placeholder="চাল (৫ কেজি)&#10;দুধ (১ লিটার)&#10;ডিম (১২ টি)"></textarea>
            <button class="btn-primary" onclick="createList()">Create List &rarr;</button>
        </div>

        <!-- Section 2: Checkboxes and Price Card -->
        <div class="card" id="list-card" style="display: none;">
            <div class="card-header">
                <span class="card-title">2. Select & Enter Prices</span>
                <button class="btn-link btn-edit" onclick="showInputCard()">[Edit Items]</button>
            </div>
            <div id="items-container"></div>
        </div>

        <!-- Generate Bill Button -->
        <button class="btn-primary btn-success" id="btn-generate" style="display: none;" onclick="generateBill()">
            Generate & Download PDF Bill
        </button>

        <!-- Hidden Invoice Rendered for Printing -->
        <div id="printable-receipt">
            <h2>Official Receipt</h2>
            <div class="receipt-date" id="receipt-date"></div>
            <table class="receipt-table">
                <thead>
                    <tr>
                        <th>Item</th>
                        <th>Price</th>
                    </tr>
                </thead>
                <tbody id="receipt-body"></tbody>
            </table>
            <div class="receipt-total">
                <span>TOTAL AMOUNT:</span>
                <span id="receipt-total-price">Rs. 0.00</span>
            </div>
        </div>
    </div>

    <script>
        // Set Auto Date and Time
        function updateDateTime() {
            const now = new Date();
            const options = { day: '2-digit', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit', hour12: true };
            const formattedDate = now.toLocaleString('en-US', options).replace(',', ' |');
            document.getElementById('live-date-time').innerText = "Date: " + formattedDate;
            return formattedDate;
        }
        
        const currentDateStr = updateDateTime();

        function clearInput() {
            document.getElementById('text-input').value = '';
        }

        // Lock text box and convert lines to interactive list
        function createList() {
            const rawText = document.getElementById('text-input').value.trim();
            if (!rawText) {
                alert("Please write at least one item!");
                return;
            }

            const lines = rawText.split('\n').map(line => line.trim()).filter(line => line.length > 0);
            const container = document.getElementById('items-container');
            container.innerHTML = '';

            lines.forEach((line, index) => {
                const row = document.createElement('div');
                row.className = 'item-row';
                row.innerHTML = `
                    <div class="item-left">
                        <input type="checkbox" id="item-${index}" checked>
                        <label for="item-${index}">${line}</label>
                    </div>
                    <div class="price-container">
                        <span>Rs.</span>
                        <input type="number" class="price-input" value="0" min="0" placeholder="0">
                    </div>
                `;
                container.appendChild(row);
            });

            // Hide input card and show list + bill button
            document.getElementById('input-card').style.display = 'none';
            document.getElementById('list-card').style.display = 'block';
            document.getElementById('btn-generate').style.display = 'block';
        }

        // Return back to text input to make changes
        function showInputCard() {
            document.getElementById('input-card').style.display = 'block';
        }

        // Collect selected items and trigger print/PDF dialog
        function generateBill() {
            const rows = document.querySelectorAll('.item-row');
            const receiptBody = document.getElementById('receipt-body');
            receiptBody.innerHTML = '';

            let total = 0;
            let count = 0;

            rows.forEach(row => {
                const isChecked = row.querySelector('input[type="checkbox"]').checked;
                if (isChecked) {
                    const itemName = row.querySelector('label').innerText;
                    const priceValue = parseFloat(row.querySelector('.price-input').value) || 0;

                    total += priceValue;
                    count++;

                    const tr = document.createElement('tr');
                    tr.innerHTML = `
                        <td>${itemName}</td>
                        <td>Rs. ${priceValue.toFixed(2)}</td>
                    `;
                    receiptBody.appendChild(tr);
                }
            });

            if (count === 0) {
                alert("No items selected!");
                return;
            }

            document.getElementById('receipt-date').innerText = "Date: " + currentDateStr;
            document.getElementById('receipt-total-price').innerText = "Rs. " + total.toFixed(2);

            // Trigger system browser print (Save as PDF)
            window.print();
        }
    </script>
</body>
</html> 
