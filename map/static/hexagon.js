console.log("Initializing new game...");

var GLOBALS = {
    "DEBUG": false,
    "gameState": "new",
    "gameID": 1,
    "colors": {
        "tundra": "white",
        "grassland": "green",
        "water": "blue",
        "mountains": "brown"
    }
};


    hex.init = function() {
        console.log("Initializing new game...");
        hex.radius = null;
        hex.height = null;
        hex.width = null;
        hex.side = null;
        hex.canvas = document.getElementById("HexCanvas");
        hex.ctx = null;
        hex.hexes = [];
        this.radius = 20;
        this.side = Math.round((3 / 2) * this.radius);
        this.height = Math.round(Math.sqrt(3) * this.radius);
        this.width = Math.round(2 * this.radius);

        /*
        Set Size of main div to size of canvas
        $('#primary-panel').css('height', (hex.height * hex.rows)+hex.height*2);
        hex.canvas.style.width='100%';
        hex.canvas.style.height='100%';
        */

        hex.canvas.width  = hex.canvas.offsetWidth;
        hex.canvas.height = hex.canvas.offsetHeight;

        //Set click eventlistener for canvas
        this.canvas.addEventListener("mousedown", this.clickEvent.bind(this), false);

        //Defines the hexes array, which provides the structure
        if(GLOBALS.gameState == "new"){
            this.defineHexGrid(this.rows, this.cols);
        }

        this.ctx = this.canvas.getContext('2d');

        //Draw base grid, then draw overlaid items on top
        this.drawHexGrid(this.rows, this.cols);

    }
    hex.draw = function() {
        this.canvas.width = this.canvas.width; //clear canvas
        this.drawHexGrid(this.rows, this.cols);
    }
    hex.rowcolToXY = function(row, col){
        var offsetColumn = (col % 2 == 0) ? false : true;
        if (!offsetColumn) {
            x = (col * this.side) + this.canvasOriginX;
            y = (row * this.height) + this.canvasOriginY;
        } else {
            x = col * this.side + this.canvasOriginX;
            y = (row * this.height) + this.canvasOriginY + (this.height * 0.5);
        }

        return {x: x, y: y}
    }
    hex.defineHexGrid = function(rows, cols) {
        var terrains = ["grassland", "mountains", "water", "tundra"];
        this.canvasOriginX = this.canvas.getBoundingClientRect().left;
        this.canvasOriginY = this.canvas.getBoundingClientRect().top;
        var currentHexX;
        var currentHexY;
        var offsetColumn = false;
        for (var col = 0; col < cols; col++) {
            this.hexes.push([]);
            for (var row = 0; row < rows; row++) {
                var currentTerrain = terrains[Math.floor(Math.random()*terrains.length)];
                if (!offsetColumn) {
                    currentHexX = (col * this.side) + this.canvasOriginX;
                    currentHexY = (row * this.height) + this.canvasOriginY;
                } else {
                    currentHexX = col * this.side + this.canvasOriginX;
                    currentHexY = (row * this.height) + this.canvasOriginY + (this.height * 0.5);
                }
                /*
                h: highlighted
                row: row
                col: column
                t: terrain type
                tc: terrain color
                txt: text written on hex
                bor: borders
                own: current owner
                u: units
                */
                this.hexes[col].push({
                    "h": false,
                    "row": row,
                    "col": col,
                    "x": this.rowcolToXY(row, col).x,
                    "y": this.rowcolToXY(row, col).y,
                    "t": currentTerrain,
                    "tc": GLOBALS.colors[currentTerrain],
                    "txt": col + "," + row,
                    "bor": {
                        "n": null,
                        "s": null,
                        "nw": null,
                        "sw": null,
                        "ne": null,
                        "se": null
                    },
                    "own": null,
                    "u": null,
                });
            }
            offsetColumn = !offsetColumn;
        }
        hex.saveData("saveAll", this.hexes);
    }
    hex.drawHexGrid = function(rows, cols) {
        //base grid
        for (var i = 0; i < cols; i++) {
            for (var j = 0; j < rows; j++) {
                this.drawHex(this.hexes[i][j].x, this.hexes[i][j].y, this.hexes[i][j].tc, this.hexes[i][j].txt, false);
            }
        }

        //overlay items
        for (var i = 0; i < cols; i++) {
            for (var j = 0; j < rows; j++) {
                if (this.hexes[i][j].h == true) {
                    this.drawHex(this.hexes[i][j].x, this.hexes[i][j].y, this.hexes[i][j].tc, this.hexes[i][j].txt, true);
                }
            }
        }

        if (GLOBALS.DEBUG == true) {
            console.log(this.hexes);
        }


    }
    hex.drawHex = function(x0, y0, fillColor, hexText, highlight) {
        if (highlight == true) {
            this.ctx.strokeStyle = "#00F2FF";
            this.ctx.lineWidth = 4;
        } else {
            this.ctx.strokeStyle = "#000";
            this.ctx.lineWidth = 2;
        }

        this.ctx.beginPath();
        this.ctx.moveTo(x0 + this.width - this.side, y0);
        this.ctx.lineTo(x0 + this.side, y0);
        this.ctx.lineTo(x0 + this.width, y0 + (this.height / 2));
        this.ctx.lineTo(x0 + this.side, y0 + this.height);
        this.ctx.lineTo(x0 + this.width - this.side, y0 + this.height);
        this.ctx.lineTo(x0, y0 + (this.height / 2));
        if (highlight == true) {}
        if (fillColor && highlight == false) {
            this.ctx.fillStyle = fillColor;
            this.ctx.fill();
        }
        this.ctx.closePath();
        this.ctx.stroke();
        if (hexText) {
            this.ctx.font = "5px";
            this.ctx.fillStyle = "#000";
            this.ctx.fillText(hexText, x0 + (this.width / 2) - (this.width / 4), y0 + (this.height - 5));
        }
    }
    hex.drawHexBorders = function() {

    }
    hex.getRelativeCanvasOffset = function() {
        var x = 0,
            y = 0;
        var layoutElement = this.canvas;
        if (layoutElement.offsetParent) {
            do {
                x += layoutElement.offsetLeft;
                y += layoutElement.offsetTop;
            } while (layoutElement = layoutElement.offsetParent);
            return {
                x: x,
                y: y
            };
        }
    }
    hex.getSelectedTile = function(mouseX, mouseY) {
        var offSet = this.canvas.getBoundingClientRect();
        mouseX -= offSet.left;
        mouseY -= offSet.top;

        var column = Math.floor((mouseX) / this.side);
        var row = Math.floor(column % 2 == 0 ? Math.floor((mouseY) / this.height) : Math.floor(((mouseY + (this.height * 0.5)) / this.height)) - 1);

        //Test if on left side of frame
        if (mouseX > (column * this.side) && mouseX < (column * this.side) + this.width - this.side) {
            //Now test which of the two triangles we are in
            //Top left triangle points
            var p1 = new Object();
            p1.x = column * this.side;
            p1.y = column % 2 == 0 ? row * this.height : (row * this.height) + (this.height / 2);

            var p2 = new Object();
            p2.x = p1.x;
            p2.y = p1.y + (this.height / 2);

            var p3 = new Object();
            p3.x = p1.x + this.width - this.side;
            p3.y = p1.y;

            var mousePoint = new Object();
            mousePoint.x = mouseX;
            mousePoint.y = mouseY;

            if (this.isPointInTriangle(mousePoint, p1, p2, p3)) {
                column--;
                if (column % 2 != 0) {
                    row--;
                }
            }

            //Bottom left triangle points
            var p4 = new Object();
            p4 = p2;

            var p5 = new Object();
            p5.x = p4.x;
            p5.y = p4.y + (this.height / 2);

            var p6 = new Object();
            p6.x = p5.x + (this.width - this.side);
            p6.y = p5.y;

            if (this.isPointInTriangle(mousePoint, p4, p5, p6)) {
                column--;

                if (column % 2 == 0) {
                    row++;
                }
            }
        }
        return {
            row: row,
            col: column
        };
    }
    hex.isPointInTriangle = function(pt, v1, v2, v3) {
        var b1, b2, b3;
        b1 = this.sign(pt, v1, v2) < 0.0;
        b2 = this.sign(pt, v2, v3) < 0.0;
        b3 = this.sign(pt, v3, v1) < 0.0;
        return ((b1 == b2) && (b2 == b3));
    }
    hex.sign = function(p1, p2, p3) {
        return (p1.x - p3.x) * (p2.y - p3.y) - (p2.x - p3.x) * (p1.y - p3.y);
    }
    hex.clickEvent = function(e) {
        var mouseX = e.pageX - window.pageXOffset;
        var mouseY = e.pageY - window.pageYOffset;
        var localX = mouseX - this.canvasOriginX;
        var localY = mouseY - this.canvasOriginY;
        var tile = this.getSelectedTile(localX, localY);
        if (GLOBALS.DEBUG == true) {
            console.log(tile);
        }
        if (tile.row < this.rows && tile.row >= 0 && tile.col < this.cols && tile.col >= 0) {
            //console.log(tile);
            this.hexes[tile.col][tile.row].h = this.hexes[tile.col][tile.row].h ? false : true;
            console.log(hex.hexes[tile.col][tile.row]);
            console.log(hex.toCubeCoord(tile.col, tile.row));
            this.draw();
        } else {
            console.log("Click out of range");
        }

    }
    hex.clearMap = function(){
        this.hexes = [];
        this.defineHexGrid(this.rows, this.cols);
        this.draw()
    }


    hex.saveData = function(param, map) {
        if (param == "saveAll"){
            var save = {
                param: "saveAll",
                data: JSON.stringify(map)
            };
            $.ajax({
                type: "POST",
                url: "save.php",
                data: save,
                dataType: 'JSON',
                success: function(data) {
                    if(data == "Success"){
                        console.log("Connected to db.");
                    }
                }
            })
        }
    }
    hex.toCubeCoord = function(q, r) {
        /**  Function to convert odd-q offset coordinates to cube coordinates. Reference: http://www.redblobgames.com/grids/hexagons/
         * @param {Number} q - the column of the hex
         * @param {Number} r - the row of the hex
         */
        this.r = r;
        this.q = q;
        var x = this.q
        var z = this.r - (this.q - (this.q & 1)) / 2
        var y = -x - z
        var cube = {
            x: x,
            y: y,
            z: z
        };

        return cube;
    }
    hex.toOffsetCoord = function(x, y, z) {
        /**  Function to convert cube coordinates to odd-q offset coordinates. Reference: http://www.redblobgames.com/grids/hexagons/
         * @param {Number} x - the x cube coord of the hex
         * @param {Number} y - the y cube coord of the hex
         * @param {Number} z - the z cube coord of the hex
         */
        this.x = x;
        this.y = y;
        this.z = z;
        var q = this.x;
        var r = this.z + (this.x - (this.x & 1)) / 2
        var offset = {
            q: q,
            r: r
        };

        return offset;
    }
    hex.getNeighbors = function(x, y, z) {
        /**  Function to find all neighboring hexes via cube coordinates. Reference: http://www.redblobgames.com/grids/hexagons/
         * @param {Number} x - the x cube coord of the hex
         * @param {Number} y - the y cube coord of the hex
         * @param {Number} z - the z cube coord of the hex
         */
        this.x = x;
        this.y = y;
        this.z = z;
        var neighbors = [{
            x: this.x + 1,
            y: this.y - 1,
            z: z
        }, {
            x: this.x + 1,
            y: y,
            z: this.z - 1
        }, {
            x: x,
            y: this.y + 1,
            z: this.z - 1
        }, {
            x: this.x - 1,
            y: this.y + 1,
            z: z
        }, {
            x: this.x - 1,
            y: y,
            z: this.z + 1
        }, {
            x: x,
            y: this.y - 1,
            z: this.z + 1
        }];
        var chk = toOffsetCoord(x, y, z);
        if (typeof(map.data[chk.r][chk.q].connect) != "undefined" || map.data[chk.r][chk.q].connect != "") {
            for (i = 0; i < map.data[chk.r][chk.q].connect.length; i++) {
                var tmp = toCubeCoord(map.data[chk.r][chk.q].connect[i].col, map.data[chk.r][chk.q].connect[i].row);
                neighbors.push(tmp);
            }
        }

        return neighbors;
    }

    hex.getDirection = function(x1, x2, y1, y2, z1, z2) {
        var delX = 0;
        var delY = 0;
        var delZ = 0;
        delX = x1 - x2;
        delY = y1 - y2;
        delZ = z1 - z2;
        var direction = "";
        if (delX == 0 && delY == 1 && delZ == -1) {
            return "n";
        }
        if (delX == 1 && delY == 0 && delZ == -1) {
            return "ne";
        }
        if (delX == 1 && delY == -1 && delZ == 0) {
            return "se";
        }
        if (delX == 0 && delY == -1 && delZ == 1) {
            return "s";
        }
        if (delX == -1 && delY == 0 && delZ == 1) {
            return "sw";
        }
        if (delX == -1 && delY == 1 && delZ == 0) {
            return "nw";
        }
    }

    hex.shuffle = function (array) {
        /* Shuffles array values randomly
        @param {Array} array
        */
        var currentIndex = array.length,
            temporaryValue, randomIndex;

        // While there remain elements to shuffle...
        while (0 !== currentIndex) {

            // Pick a remaining element...
            randomIndex = Math.floor(Math.random() * currentIndex);
            currentIndex -= 1;

            // And swap it with the current element.
            temporaryValue = array[currentIndex];
            array[currentIndex] = array[randomIndex];
            array[randomIndex] = temporaryValue;
        }

        return array;
    }

    hex.init();