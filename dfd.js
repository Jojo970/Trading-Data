const dfd = require('danfojs-node');

let time = [];

const convertTime = (series) => {

    const times = series.values

    times.forEach(element => {
        let date = new Date(element)
        time.push(date)
    });


    // for(let i =0; i < length; i++){

    //     let date = new Date(series.iloc([i])['$data'][0])
    //     time.push(date)
    //     // console.log(series.iloc([i])['$data'][0])
    // }
    return time
}

const simpleMovingAverage = (series, period) => {

    let prices = series.values

    let i = 0
    let sum = 0

    while(i < period){
        sum = sum + (prices[i] * 1)
        i++
    }

    const sma = sum/period

    return sma
}


const estimatedMovingAverage = (series, sma, period) => {
    // EMA = Closing price x multiplier + EMA (previous day) x (1-multiplier)

    // multiplier = [2 ÷ (period + 1)]

    const multiplier = [2 / (period + 1)]

    let priceArray = series.values

    let emaArray = [];
    let num = 0

    while(num < (period-1)) {
        emaArray.push(NaN)
        num++
    }

    emaArray.push(sma)

    while(num < (priceArray.length - 1)){
        let nums = num - 1
        let ema = (priceArray[num] * 1) * multiplier + emaArray[num] * (1 - multiplier)
        emaArray.push(ema)
        num++
    }

    return emaArray
}



!async function() {

    let x = await fetch('https://api.binance.us/api/v3/klines?symbol=LTCUSDT&interval=1d&limit=50').then(res => res.json()).then(data => {
                df = new dfd.DataFrame(data);
                return df
            })
    
    // x.print()
    let converted = convertTime(x[0])
    x.addColumn('12', converted, { inplace:true })
    x.drop({ columns: ['0', '11'], inplace : true})
    let num = 10

    const sma = simpleMovingAverage(x[4], num)
    
    const emaArrayToAppend = estimatedMovingAverage(x[4], sma, num)

    console.log(emaArrayToAppend.length, "ema", emaArrayToAppend)

    x.addColumn('EMA', emaArrayToAppend, { inplace:true })

    let check = x.iloc({rows:[15]})

    check.print()
    // console.log(x.iloc({rows: [num]})['$data'][0])
}();

// df = new dfd.DataFrame(x)

// df.print()
