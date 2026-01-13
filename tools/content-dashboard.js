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
var watch_data = []
var likes_data = []
var comments_data = []
var view_sum  = 0
var wtime_sum  = 0
var like_sum  = 0
var comments_sum  = 0
for(i=28;i>0;i-=1){
    var d = new Date(new Date().setDate(today.getDate() - i))
    var vw = Math.floor((Math.random() * 10000) + 1)
    var wt = Math.floor((Math.random() * 100) + 1)
    var lk = Math.floor((Math.random() * 1000) + 1)
    var cm = Math.floor((Math.random() * 300) + 1)
    views_data.push([d.getTime(),vw])
    watch_data.push([d.getTime(),wt])
    likes_data.push([d.getTime(),lk])
    comments_data.push([d.getTime(),cm])
    view_sum += vw
    wtime_sum += wt
    like_sum += lk
    comments_sum += cm
}

let formatter = Intl.NumberFormat('en', { notation: 'compact' });

Highcharts.chart('view-chart', {
    title: {
        text: 'Your channel got '+formatter.format(view_sum)+' Views in last 28 Days'
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
        name: 'Views',
        type: 'area',
        data: views_data,
        marker:{
            radius:0
        },
        color:'#ff6363'
    }],
    
});

Highcharts.chart('watch-chart', {
    title: {
        text: 'Your channel got '+formatter.format(wtime_sum)+' hours of Watch Time in last 28 Days'
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

        name: 'Watch Time',
        type: 'area',
        data: watch_data,
        marker:{
            radius:0
        },
        color:'#ff6363'
    }],
    
});

Highcharts.chart('likes-chart', {
    title: {
        text: 'Your channel got '+formatter.format(like_sum)+' Likes & '+formatter.format(comments_sum)+' Comments in last 28 Days'
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
        name: 'Likes',
        type: 'column',
        data: likes_data,
        marker:{
            radius:0
        },
        color:'#ff6363'
    },{
        name: 'Comments',
        type: 'column',
        data: comments_data,
        marker:{
            radius:0
        },
        color:'#800e0e'
    }],
    
});

Highcharts.chart('youtube-source', {
    chart: {
        plotBackgroundColor: null,
        plotBorderWidth: null,
        plotShadow: false,
        type: 'pie'
    },
    title: {
        text: ''
    },
    tooltip: {
        formatter: function () {
            return this.point.series.name+': ' + this.point.options.y;            
        }
    },
    accessibility: {
        point: {
            valueSuffix: '%'
        }
    },
    plotOptions: {
        pie: {
            allowPointSelect: true,
            cursor: 'pointer',
            dataLabels: {
                enabled: true,
                format: '<b>{point.name}</b>: {point.percentage:.1f} %'
            }
        }
    },
    series: [{
        name: 'Source',
        colorByPoint: true,
        data: [{
            name: 'YouTube Search',
            y: 73.5,
            sliced: true,
            selected: true
        }, {
            name: 'Shorts Feed',
            y: 2.7
        },  {
            name: 'Oth­er You­Tube fea­tures',
            y: 12.8
        }, {
            name: 'External',
            y: 1.8
        }, {
            name: 'Playlist Page',
            y: 0.3
        },  {
            name: 'Others',
            y: 10.9
        }]
    }]
});
              
