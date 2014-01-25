var width = 960;
var height = 136;
var cellSize = 17;

var day = d3.time.format("%w");
var week = d3.time.format("%U");
var percent = d3.format("d");
var format = d3.time.format("%Y-%m-%d");

var color = d3.scale.linear().domain([0, 10000]).range([0, 1.0]);

    var svg = d3.select("body").selectAll("svg")
    .data(d3.range(2010, 2015))
    .enter().append("svg")
    .attr("width", width)
    .attr("height", height)
    .attr("class", "RdYlGn")
    .append("g")
    .attr("transform", "translate(" + ((width - cellSize * 53) / 2) + "," + (height - cellSize * 7 - 1) + ")");

    svg.append("text")
    .attr("transform", "translate(-6," + cellSize * 3.5 + ")rotate(-90)")
    .style("text-anchor", "middle")
    .text(function(d) { return d; });

    var rect = svg.selectAll(".day")
    .data(function(d) { return d3.time.days(new Date(d, 0, 1), new Date(d + 1, 0, 1)); })
    .enter().append("rect")
    .attr("class", "day")
    .attr("width", cellSize)
    .attr("height", cellSize)
    .attr("x", function(d) { return week(d) * cellSize; })
    .attr("y", function(d) { return day(d) * cellSize; })
    .datum(format);

    rect.append("title")
    .text(function(d) { return d; });

    svg.selectAll(".month")
    .data(function(d) { return d3.time.months(new Date(d, 0, 1), new Date(d + 1, 0, 1)); })
    .enter().append("path")
    .attr("class", "month")
    .attr("d", monthPath);

    d3.csv("dji.csv", function(error, csv) {
        var data = d3.nest().key(function(d) {
            return d.Date;
        }).rollup(function(d) {
            //return (d[0].Close - d[0].Open) / d[0].Open;
            return d[0].Amount;
        }).map(csv);

        rect.filter(function(d) {
            return d in data;
        }).attr("style", function(d) {
            var code = ColorScaleBCGYR(color(data[d]));
            var code2 = code.toString(16);
            return "fill:#" + fillZero(code2);
        }).select("title").text(function(d) {
            return d + ": " + percent(data[d]);
        });
    });

function fillZero(num) {
    var c = 6 - num.length;
    if (c <=0 ) {
        return num;
    }
    var z = '';
    for(var i=0;i<c;i++) {
        z += '0';
    }
    return z + num;
}

// http://qiita.com/krsak/items/94fad1d3fffa997cb651
function ColorScaleBCGYR( in_value ) {
    // 0.0～1.0 の範囲の値をサーモグラフィみたいな色にする
    // 0.0                    1.0
    // 青    水    緑    黄    赤
    // 最小値以下 = 青
    // 最大値以上 = 赤
    var a = 255;    // alpha値
    var r, g, b;    // RGB値
    var  value = in_value;
    var  tmp_val = Math.cos( 4 * Math.PI * value );

    var col_val = Math.ceil( ( -tmp_val / 2 + 0.5 ) * 255 );
    if ( value >= ( 4.0 / 4.0 ) ) { r = 255; g = 0; b = 0; }   // 赤
    else if ( value >= ( 3.0 / 4.0 ) ) { r = 255;     g = col_val; b = 0;       }   // 黄～赤
    else if ( value >= ( 2.0 / 4.0 ) ) { r = col_val; g = 255;     b = 0;       }   // 緑～黄
    else if ( value >= ( 1.0 / 4.0 ) ) { r = 0;       g = 255;     b = col_val; }   // 水～緑
    else if ( value >= ( 0.0 / 4.0 ) ) { r = 0;       g = col_val; b = 255;     }   // 青～水
    else {                               r = 0;       g = 0;       b = 255;     }   // 青
    var ret = (r&0x000000FF) << 16
        | (g&0x000000FF) <<  8
        | (b&0x000000FF);
    return ret;
}

function monthPath(t0) {
    var t1 = new Date(t0.getFullYear(), t0.getMonth() + 1, 0),
        d0 = +day(t0), w0 = +week(t0),
        d1 = +day(t1), w1 = +week(t1);
    return "M" + (w0 + 1) * cellSize + "," + d0 * cellSize
        + "H" + w0 * cellSize + "V" + 7 * cellSize
        + "H" + w1 * cellSize + "V" + (d1 + 1) * cellSize
        + "H" + (w1 + 1) * cellSize + "V" + 0
        + "H" + (w0 + 1) * cellSize + "Z";
}

d3.select(self.frameElement).style("height", "2910px");
