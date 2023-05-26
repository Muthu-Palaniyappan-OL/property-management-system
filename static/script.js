document.querySelectorAll('.bg-danger').forEach((button) => button.addEventListener('click', (event) => {
    const id = event.target.parentElement.parentElement.parentElement.innerText
    console.log(id)
    if (id === "") return
    fetch('/deleteuser', {
        headers: {
            "Content-Type": "application/json",
        },
        method: 'post',
        body: JSON.stringify({ username: id }),
    }).then(e => {
        console.log(e)
        if (window.history.replaceState) {
            window.history.replaceState(null, null, window.location.href);
        }
        location.reload()
    }).catch(e => {
        console.log(e)
    })
}))

function delete_vendor(property_name, vendor_name) {
    fetch(`/deletevendor/${property_name}/${vendor_name}`, {
        headers: {
            "Content-Type": "application/json",
        },
        method: 'delete',
    }).then(e => {
        console.log(e)
    }).catch(e => {
        console.log(e)
    })
    window.location.href = `/`+window.location.href.split('/')[3]+'/'+window.location.href.split('/')[4];
}

function request_invoice(event, property_name, vendor_name) {
    fetch(`/sendinvoice/${property_name}/${vendor_name}}/${event.target.parentElement.parentElement.querySelector('#invoiceAmount').value}`, {
        headers: {
            "Content-Type": "application/json",
        },
        method: 'get',
    }).then(e => {
        console.log(e)
        window.location.href = `/`;
    }).catch(e => {
        console.log(e)
    })
    window.location.href = `/`+window.location.href.split('/')[3]+'/'+window.location.href.split('/')[4];
}

function edit_vendor(property_name, vendor_name) {
    window.location.href = `/editvendor/${property_name}/${vendor_name}`;
}

const expense_type = `<option value="COGS">COGS</option>
<option value="Operating Expenses">Operating Expenses</option>
<option value="Depreciation and Amortization">Depreciation and Amortization</option>
<option value="Interest Expense">Interest Expense</option>
<option value="Taxes">Taxes</option>`

const income_type = `<option selected value="Rental Income">Rental Income</option>
<option value="Sales Revenue">Sales Revenue</option>
<option value="Interest Income">Interest Income</option>
<option value="Licensing and Royalty Income">Licensing and Royalty Income</option>
<option value="Other Income">Other Income</option>`

expense_data = {
    'COGS': 0,
    'Operating Expenses': 0,
    'Depreciation and Amortization': 0,
    'Interest Expense': 0,
    'Taxes': 0,
}

income_data = {
    'Rental Income': 0,
    'Sales Revenue': 0,
    'Interest Income': 0,
    'Licensing and Royalty Income': 0,
    'Other Income': 0,
}

finance_data = []

document.querySelector('#direction').onchange = () => {
    const choice = document.querySelector('#direction').value
    console.log(choice)
    if (choice == 'income')
        document.querySelector('#type').innerHTML = income_type
    if (choice == 'expense')
        document.querySelector('#type').innerHTML = expense_type
}

document.addEventListener('DOMContentLoaded', () => {
    const data = document.querySelector('#finance-data').innerText
    if (data == '' || data == 'None' || data == []) {
        finance_data = []
    } else {
        finance_data = JSON.parse(data)
    }
    for (let i=0;i<finance_data.length;++i){
        const table_element_item = `<tr><td>${finance_data[i].name}</td><td>${finance_data[i].dir}</td><td>${finance_data[i].type}</td><td>${finance_data[i].amount}</td></tr>`
        document.querySelector('#finance-table-body').insertAdjacentHTML('afterbegin', table_element_item);
    }

    income_chart_update()
    expense_chart_update()
})

function addItem() {
    const name = document.querySelector('#name').value
    const dir = document.querySelector('#direction').value
    const type = document.querySelector('#type').value
    const amount = document.querySelector('#amount').value
    const table_element_item = `<tr><td>${name}</td><td>${dir}</td><td>${type}</td><td>${amount}</td></tr>`
    finance_data.push({
        name,
        dir,
        type,
        amount
    })
    console.log(finance_data)
    property_name = /\/property\/([a-zA-Z0-9]+)/.exec(window.location.href)[1]
    fetch(`/property/${property_name}/finance`, {
        method: 'POST',
        body: JSON.stringify(finance_data)
    })
    document.querySelector('#finance-table-body').insertAdjacentHTML('afterbegin', table_element_item);
    income_chart_update()
    expense_chart_update()
}

function income_chart_update() {
    google.charts.load('current', {'packages':['corechart']});
    google.charts.setOnLoadCallback(drawChart);

  function drawChart() {
    // Create the data table
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Label');
    data.addColumn('number', 'Value');
    map = {}
    for(let i=0;i<finance_data.length;++i) {
        if (finance_data[i].dir == 'income') {
            if (map[finance_data[i].type] == undefined){
                map[finance_data[i].type] = parseInt(finance_data[i].amount)
            } else {
                map[finance_data[i].type] += parseInt(finance_data[i].amount)
            }
        }
    }

    for(let key in map) {
        data.addRows([
            [key, map[key]]
        ]);
    }

    // Set chart options
    var options = {
      title: 'Income Chart',
    };

    // Instantiate and draw the chart
    var chart = new google.visualization.PieChart(document.getElementById('income_chart'));
    chart.draw(data, options);
  }
}

function expense_chart_update() {
    google.charts.load('current', {'packages':['corechart']});
    google.charts.setOnLoadCallback(drawChart);

  function drawChart() {
    // Create the data table
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Label');
    data.addColumn('number', 'Value');
    map = {}
    for(let i=0;i<finance_data.length;++i) {
        if (finance_data[i].dir == 'expense') {
            if (map[finance_data[i].type] == undefined){
                map[finance_data[i].type] = parseInt(finance_data[i].amount)
            } else {
                map[finance_data[i].type] += parseInt(finance_data[i].amount)
            }
        }
    }

    for(let key in map) {
        data.addRows([
            [key, map[key]]
        ]);
    }

    // Set chart options
    var options = {
      title: 'Expense Chart',
    };

    // Instantiate and draw the chart
    var chart = new google.visualization.PieChart(document.getElementById('expense_chart'));
    chart.draw(data, options);
  }
}