export const combineBase = {
    color: ['#0595e5', 'rgba(255,234,0)',],
    title: {
        text: '趋势组合图',
        textStyle: {
            fontSize: '1rem'
        }
    },
    tooltip: {
        trigger: 'axis', // 按坐标轴触发，同时显示 bar 和 line 的数据
        axisPointer: {
            type: 'cross' // 交叉指针，便于查看数据
        },

    },
    legend: {
        data: ['销量', '价格'] // 图例
    },
    grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
    },
    xAxis: [{
        type: 'category',
        data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    }],
    yAxis: [
        {
            type: 'value',
            name: '销量 (件)', // 左侧 Y 轴名称
        },
        {
            type: 'value',
            name: '价格 (元)', // 右侧 Y 轴名称

        }
    ],
    series: [
        {
            data: [150, 230, 224, 218, 135, 147, 260],
            type: 'line',
            yAxisIndex: 0,
            symbolSize: 8,
        },
        {
            data: [150, 230, 224, 218, 135, 147, 260],
            type: 'bar',
            yAxisIndex: 1
        }
    ]
}