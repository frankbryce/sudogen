var socket = io();

// for debugging
socket.on('connect', function() {
    console.log('socket is open');
});
socket.on('disconnect', function() {
    console.log('socket is closed');
});

let brick_sz = 28;
let gridSelect = d3.select('body')
    .append('svg')
        .attr("width", 24*brick_sz)
        .attr("height", 24*brick_sz);

function AddRect(sel,w,h,x,y,f,s=1,o=1.0) {
    console.log('AddRect ', 2, h, x, y, f, s);
    return sel.append('rect')
        .attr("width", w*brick_sz)
        .attr('height', h*brick_sz)
        .attr('x', x*brick_sz)
        .attr('y', y*brick_sz)
        .attr('fill', f)
        .attr('stroke', f != 'black' ? 'black' : LIGHT_GREY)
        .attr('stroke-width', s)
        .attr('opacity', o);
}

function AddCirc(sel,r,x,y,f,b) {
    return sel.append('circle')
        .attr('r', r*brick_sz)
        .attr('cx', x*brick_sz)
        .attr('cy', y*brick_sz)
        .attr('fill', f)
        .attr('stroke-width', 1)
        .attr('stroke', b);
        
}

DARK_GREY = '#666'
LIGHT_GREY = '#bbb'
BOX_BG = '#222'

// grid frame
AddRect(gridSelect,8,1,0,0,DARK_GREY, 1.5, 1.0);
AddRect(gridSelect,8,1,8,0,'yellow', 1.5, 1.0);
AddRect(gridSelect,8,1,16,0,DARK_GREY, 1.5, 1.0);
AddRect(gridSelect,1,8,0,1,DARK_GREY, 1.5, 1.0);
AddRect(gridSelect,1,6,0,9,'yellow', 1.5, 1.0);
AddRect(gridSelect,1,8,0,15,DARK_GREY, 1.5, 1.0);
AddRect(gridSelect,1,8,23,1,DARK_GREY, 1.5, 1.0);
AddRect(gridSelect,1,6,23,9,'yellow', 1.5, 1.0);
AddRect(gridSelect,1,8,23,15,DARK_GREY, 1.5, 1.0);
AddRect(gridSelect,8,1,0,23,DARK_GREY, 1.5, 1.0);
AddRect(gridSelect,8,1,8,23,'yellow', 1.5, 1.0);
AddRect(gridSelect,8,1,16,23,DARK_GREY, 1.5, 1.0);
AddRect(gridSelect,2,22,7,1,LIGHT_GREY, 1.5, 1.0);
AddRect(gridSelect,2,22,15,1,LIGHT_GREY, 1.5, 1.0);
AddRect(gridSelect,22,2,1,7,LIGHT_GREY, 1.5, 1.0);
AddRect(gridSelect,22,2,1,15,LIGHT_GREY, 1.5, 1.0);

function AddBox(basex, basey) {
    AddRect(gridSelect,6,6,basex,basey,BOX_BG);
    AddCirc(gridSelect,0.3,basex+1,basey+1,'blue','black');
    AddCirc(gridSelect,0.3,basex+3,basey+1,'blue','black');
    AddCirc(gridSelect,0.3,basex+5,basey+1,'blue','black');
    AddCirc(gridSelect,0.3,basex+1,basey+3,'blue','black');
    AddCirc(gridSelect,0.3,basex+3,basey+3,'blue','black');
    AddCirc(gridSelect,0.3,basex+5,basey+3,'blue','black');
    AddCirc(gridSelect,0.3,basex+1,basey+5,'blue','black');
    AddCirc(gridSelect,0.3,basex+3,basey+5,'blue','black');
    AddCirc(gridSelect,0.3,basex+5,basey+5,'blue','black');
}
AddBox(1,1);
AddBox(9,1);
AddBox(17,1);
AddBox(1,9);
AddBox(9,9);
AddBox(17,9);
AddBox(1,17);
AddBox(9,17);
AddBox(17,17);

function updateGrid(grid) {
    console.log(grid[0]);
    digit_count = 0;
    brick_colors = ['white', LIGHT_GREY, DARK_GREY, 'black', 'red', 'yellow', 'green', 'blue', 'plum'];
    for (let r=0;r<9;r++) {
        for (let c=0;c<9;c++) {
            console.log(grid[r][c]);
            if (grid[r][c] == 0) { continue; }
	    digit_count += 1;
            x = 2*c+1;
            y = 2*r+1;
            if (r>=3) { y += 2; }
            if (r>=6) { y += 2; }
            if (c>=3) { x += 2; }
            if (c>=6) { x += 2; }
            color = brick_colors[grid[r][c]-1];
            bcolor = color != 'black' ? 'black' : LIGHT_GREY;
            AddRect(gridSelect,2,2,x,y,color);
            AddCirc(gridSelect,0.25,x+0.5,y+0.5,color,bcolor);
            AddCirc(gridSelect,0.25,x+0.5,y+1.5,color,bcolor);
            AddCirc(gridSelect,0.25,x+1.5,y+0.5,color,bcolor);
            AddCirc(gridSelect,0.25,x+1.5,y+1.5,color,bcolor);
        }
    }
    console.log("updated grid with " + digit_count + " digits");
}

socket.on('json', function(data) {
    console.log(data.start);
    console.log(data.solution);
    updateGrid(JSON.parse(data.start));
    document.addEventListener('keydown', onKeyHandler);
    function onKeyHandler(e) {
	if (e.keyCode === 13) {
	    updateGrid(JSON.parse(data.solution));
	    document.removeEventListener('keydown', onKeyHandler);
	}
    }
});

function getGrid(difficulty) {
    socket.emit('grid', difficulty);
}
getGrid(10);
