const burger = document.querySelector('#burger');
const menu = document.querySelector('#menu');
burger.addEventListener('click', () => {
    if(menu.classList.contains('hidden')){
        menu.classList.remove('hidden')
    }else{
        menu.classList.add('hidden')
    }
});

const aud = document.querySelector('#aud-select');
aud.addEventListener('change', () => {
    show_chart(aud.value)
});


function viewers_chart(ud,rd){
    Highcharts.chart('aud-chart', {
        title: {
            text: 'Viewers'
        },
        tooltip: {
            formatter: function () {
                return this.point.series.name+': ' + this.point.options.y;            
            }
        },
        xAxis: {
            type: 'datetime',
            lineWidth: 1,
            lineColor: '#CCCCCC',
            labels: {
                formatter: function () {
                    return Highcharts.dateFormat('%d, %b', this.value);
                },
                align: 'center',
                x: 5,
            },
            
            showFirstLabel: true,
            showLastLabel: false,
            startOnTick: false,
            endOnTick: false
        },
        legend: {
            className: 'underline',
        },
        responsive: {
            rules: [{
                condition: {
                    maxWidth: 500
                },
                chartOptions: {
                    legend: {
                        layout: 'horizontal',
                        align: 'center',
                        verticalAlign: 'bottom'
                    }
                }
            }]
        },
        series: [{
            name: 'Unique Viewers',
            type: 'line',
            data: ud,
            marker:{
                radius:0
            },
            color:'#ff6363'
        },{
            name: 'Returning Viewers',
            type: 'line',
            data: rd,
            marker:{
                radius:0
            },
            color:'#ade915'
        },
        ],
        
    })
}

function mul_charts(title, _series){
    Highcharts.chart('aud-chart', {
        title: {
            text: title
        },
        tooltip: {
            formatter: function () {
                return this.point.series.name+': ' + this.point.options.y;            
            }
        },
        xAxis: {
            type: 'datetime',
            lineWidth: 1,
            lineColor: '#CCCCCC',
            labels: {
                formatter: function () {
                    return Highcharts.dateFormat('%d, %b', this.value);
                },
                align: 'center',
                x: 5,
            },
            showFirstLabel: true,
            showLastLabel: false,
            startOnTick: false,
            endOnTick: false
        },
        legend: {
            className: 'underline',
        },
        responsive: {
            rules: [{
                condition: {
                    maxWidth: 500
                },
                chartOptions: {
                    legend: {
                        layout: 'horizontal',
                        align: 'center',
                        verticalAlign: 'bottom'
                    }
                }
            }]
        },
        series: _series,
        
    })
}
function col_chart(title , _series){
    Highcharts.chart('aud-chart', {
        title: {
            text: title
        },
        tooltip: {
            formatter: function () {
                return this.point.category+': ' + this.point.options.y;            
            }
        },
        pointWidth:20,
        xAxis: {
            categories: ['Male', 'Female'],
            type: 'category',
            lineWidth: 1,
            lineColor: '#CCCCCC',
            showFirstLabel: true,
            showLastLabel: true,
            startOnTick: false,
            endOnTick: false
        },
        legend: {
            className: 'underline',
        },
        responsive: {
            rules: [{
                condition: {
                    maxWidth: 500
                },
                chartOptions: {
                    legend: {
                        layout: 'horizontal',
                        align: 'center',
                        verticalAlign: 'bottom'
                    }
                }
            }]
        },
        series: _series,
        
    })
}

function get_random_data(val){
    var today = new Date();
    var td = []
    for(i=28;i>0;i-=1){
        var d = new Date(new Date().setDate(today.getDate() - i))
        var rv = Math.floor((Math.random() * val) + 1)
        td.push([d.getTime(),rv])
    } 
    return td
}

function show_chart(type) {
    var today = new Date();
    let source = []
    let colors = []
    let series = []
    switch (type) {
        case 'viewers':
            let unique_data = get_random_data(10)
            let returning_data = get_random_data(100)
            viewers_chart(unique_data,returning_data)           
            break;
        case 'traffic-source':
            source = ["You­Tube search","Shorts feed","Ex­tern­al","Oth­er You­Tube fea­tures","Playl­ist page","Sug­ges­ted videos","Browse fea­tures","Hasht­ag pages","Dir­ect or un­known","Playl­ists","Sound pages","Chan­nel pages"]
            colors = ["red","yellow","green","black","purple","gray","blue","orange","lime","cyan","pink","purple"]
            series = []
            for(let i=0;i<source.length;i++){
                let stx = {
                    name: source[i],
                    type: 'line',
                    data: get_random_data(100),
                    marker:{
                        radius:0
                    },
                    color:colors[i]
                }
                series.push(stx)
            }
            mul_charts("Traffic Source", series)
            break;
        case 'top-geo':
            source = ["India","USA","United Kingdom","South Korea","Indonesia"]
            colors = ["red","yellow","purple","orange","lime",]
            series = []
            for(let i=0;i<source.length;i++){
                let stx = {
                    name: source[i],
                    type: 'line',
                    data: get_random_data(100),
                    marker:{
                        radius:0
                    },
                    color:colors[i]
                }
                series.push(stx)
            }
            mul_charts("Geography", series)
            break;
        case 'gender':
            source = ["Gender"]
            colors = ["green"]
            series = []
            for(let i=0;i<source.length;i++){
                let stx = {
                    name: source[i],
                    type: 'column',
                    data: [ Math.floor((Math.random() * 100)), Math.floor((Math.random() * 100))],
                    marker:{
                        radius:0
                    },
                    color:colors[i]
                }
                series.push(stx)
            }
            col_chart("Viewers Gender", series)
            break;
        case 'age':
            
            break
        default:
            break;
    }
}

show_chart('viewers')