export const openRankBase = {

    color: ['#34e772'],
    title: {
        text: 'OpenRank',
        textStyle:{
            fontSize: '1rem'
        }
    },
    tooltip: {
        trigger: 'axis',

    },
    xAxis: [{
        type: 'category',
        boundaryGap: false,
        data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    }],
    yAxis: {
        type: 'value'
    },
    series: [
        {
            data: [820, 932, 901, 934, 1290, 1330, 1320],
            type: 'line',
            symbolSize: 10
        }
    ]

}