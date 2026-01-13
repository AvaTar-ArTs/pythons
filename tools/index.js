const burger = document.querySelector('#burger');
const menu = document.querySelector('#menu');
burger.addEventListener('click', () => {
    if(menu.classList.contains('hidden')){
        menu.classList.remove('hidden')
    }else{
        menu.classList.add('hidden')
    }
});


var today = new Date();
var options = { year: 'numeric', month: 'long', day: 'numeric' };
var views_data = []
var sub_data = []
var likes_data = []
var comments_data = []
var view_sum  = 0
var sub_sum  = 0
var like_sum  = 0
for(i=28;i>0;i-=1){
    var d = new Date(new Date().setDate(today.getDate() - i))
    var vw = Math.floor((Math.random() * 10000) + 1)
    var sub = Math.floor((Math.random() * 100) + 1)
    var lk = Math.floor((Math.random() * 1000) + 1)
    views_data.push([d.getTime(),vw])
    sub_data.push([d.getTime(),sub+sub_sum])
    likes_data.push([d.getTime(),lk])
    view_sum += vw
    sub_sum += sub
    like_sum += lk
}

let formatter = Intl.NumberFormat('en', { notation: 'compact' });

Highcharts.chart('mview-chart', {
    title: {
        text: formatter.format(view_sum)+" Views",
        style: { "color": "green","fontSize":"12px"},
        y:40
    },
    tooltip: {
        enabled:false
    },
    yAxis: {
        labels: {
            enabled: false
        },
        visible: false,
        gridLineColor: 'transparent',
    },
    xAxis: {
        type: 'datetime',
        lineWidth: 1,
        lineColor: '#CCCCCC',
        labels: {
            enabled: false
        },
        visible: false,
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
        showInLegend:false,
        name: 'Views',
        type: 'area',
        data: views_data,
        marker:{
            radius:0
        },
        color:'#ff6363'
    }],
    
});

Highcharts.chart('mlike-chart', {
    title: {
        text: formatter.format(like_sum)+"+ Likes",
        style: { "color": "green","fontSize":"12px"},
        y:40
    },
    tooltip: {
        enabled:false
    },
    yAxis: {
        labels: {
            enabled: false
        },
        visible: false,
        gridLineColor: 'transparent',
    },
    xAxis: {
        type: 'datetime',
        lineWidth: 1,
        lineColor: '#CCCCCC',
        labels: {
            enabled: false
        },
        visible: false,
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
        showInLegend:false,
        name: 'Likes',
        type: 'area',
        data: likes_data,
        marker:{
            radius:0
        },
        color:'#0aecae'
    }],
    
});
Highcharts.chart('msub-chart', {
    title: {
        text: formatter.format(sub_sum)+"+ Subscribers",
        style: { "color": "green","fontSize":"12px"},
        y:40
    },
    tooltip: {
        enabled:false
    },
    yAxis: {
        labels: {
            enabled: false
        },
        visible: false,
        gridLineColor: 'transparent',
    },
    xAxis: {
        type: 'datetime',
        lineWidth: 1,
        lineColor: '#CCCCCC',
        labels: {
            enabled: false
        },
        visible: false,
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
        showInLegend:false,
        name: 'Subscribers',
        type: 'area',
        data: sub_data,
        marker:{
            radius:0
        },
        color:'#ade915'
    }],
    
});
