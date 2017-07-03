console.log("Initializing new game...");

var GLOBALS = {
    "DEBUG": true,
    "gameState": "new",
    "gameID": 1,
    "colors": {
        "tundra": "white",
        "grassland": "green",
        "water": "blue",
        "mountains": "brown"
    }
};

    var hex = {};
    hex.init = function() {
        // Data Pulls from API
        hex.game_info = {};
        hex.get_game_info();
        hex.hexes = [];
        for (var rows = 0; rows < hex.game_info.rows; rows++){
            hex.hexes.push([])
            for (var columns = 0; columns < hex.game_info.columns; columns++){
                hex.hexes[rows].push([]);
            }
        }
        hex.get_tiles();

        hex.canvas = document.getElementById("HexCanvas");
        hex.ctx = hex.canvas.getContext('2d');
        hex.canvas.width  = hex.canvas.offsetWidth;
        hex.canvas.height = hex.canvas.offsetHeight;
        hex.canvasOriginX = 10;
        hex.canvasOriginY = 10;

        hex.radius = 25;
        hex.side = Math.round((3 / 2) * hex.radius);
        hex.height = Math.round(Math.sqrt(3) * hex.radius);
        hex.width = Math.round(2 * hex.radius);
        hex.selected = null;
        hex.effected = null;
        hex.tiles_changed = [];
        hex.actions = [];
        hex.game_id = game_id;

        /*
        Set Size of main div to size of canvas
        $('#primary-panel').css('height', (hex.height * hex.rows)+hex.height*2);
        hex.canvas.style.width='100%';
        hex.canvas.style.height='100%';
        */

        //Set click eventlistener for canvas
        hex.canvas.addEventListener("mousedown", this.clickEvent.bind(this), false);

        //Draw base grid, then draw overlaid items on top
        hex.drawHexGrid();

    }
    hex.get_game_info = function(){
        $.ajax({
            url: '/map/games/' + game_id,
            async: false,
            dataType: 'json',
            type: "GET",
            success: function (response) {
                hex.game_info.turn_phase = response.turn_phase;
                hex.game_info.turn_player = response.turn_player;
                hex.game_info.fortifies_used = response.fortifies_used;
                hex.game_info.fortifies_remaining = response.fortifies_remaining;
                hex.game_info.rows = response.rows;
                hex.game_info.columns = response.columns;
            }
        });
    }
    hex.update_game_info = function(){
       $.ajax({
            url: '/map/games/' + game_id + '/',
            async: false,
            dataType: 'json',
            data: JSON.stringify(hex.game_info),
            type: "PUT",
            success: function (response) {
                hex.game_info.turn_phase = response.turn_phase;
                hex.game_info.turn_player = response.turn_player;
                hex.game_info.fortifies_used = response.fortifies_used;
                hex.game_info.fortifies_remaining = response.fortifies_remaining;
                hex.game_info.rows = response.rows;
                hex.game_info.columns = response.columns;
            }
        });
    }
    hex.increment_turn_phase = function(){
        if (hex.game_info.turn_phase == 'unit_placement'){
            hex.game_info.turn_phase = 'attack';
        }else if (hex.game_info.turn_phase == 'attack'){
            hex.game_info.turn_phase = 'fortify';
        }
    }
    hex.get_tiles = function(){
        $.ajax({
          url: '/map/tile_list/' + game_id,
          async: false,
          dataType: 'json',
          success: function (response) {
              response.forEach(function(tile) {
                  hex.hexes[tile.row][tile.column] = tile;
              });
          }
        });
    }
    hex.draw = function() {
        this.canvas.width = this.canvas.width; //clear canvas
        hex.drawHexGrid();
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
    hex.defineHexGrid = function() {
        var terrains = ["grassland", "mountains", "water", "tundra"];

    }
    hex.drawHexGrid = function() {
        //base grid
        for (var row = 0; row < hex.hexes.length; row++){
            for (var column = 0; column < hex.hexes[row].length; column++){
                var coords = hex.rowcolToXY(hex.hexes[row][column].row, hex.hexes[row][column].column);
                text = hex.hexes[row][column].owner + ":" + hex.hexes[row][column].units;
                hex.drawHex(coords.x, coords.y, hex.hexes[row][column].owner_color, text, false);
            }
        }

        //overlay items
        for (var row = 0; row < hex.hexes.length; row++){
            for (var column = 0; column < hex.hexes[row].length; column++){
                var coords = hex.rowcolToXY(hex.hexes[row][column].row, hex.hexes[row][column].column);
                if (hex.hexes[row][column].highlighted == true){
                    hex.drawHex(coords.x, coords.y, hex.hexes[row][column].owner_color, hex.hexes[row][column].tile_text, true, hex.hexes[row][column].highlight_color);
                }
            }
        }

    }
    hex.drawHex = function(x0, y0, fillColor, hexText, highlight, highlight_color) {
        //TODO: New draw logic? https://jsfiddle.net/6Lb8w4gr/
        if (highlight == true) {
            if (highlight_color){
                this.ctx.strokeStyle = highlight_color;
            }else{
                this.ctx.strokeStyle = "#00F2FF";
            }
            this.ctx.lineWidth = 4;
        } else {
            this.ctx.strokeStyle = "#000";
            this.ctx.lineWidth = 2;
        }

        if (highlight == true){
            this.ctx.beginPath();
            var modifier = 0.9;
            this.ctx.moveTo(x0 + (this.width*modifier) - (this.side*modifier), y0);
            this.ctx.lineTo(x0 + (this.side*modifier), y0);
            this.ctx.lineTo(x0 + (this.width*modifier), y0 + ((this.height / 2)*modifier));
            this.ctx.lineTo(x0 + (this.side*modifier), y0 + (this.height*modifier));
            this.ctx.lineTo(x0 + (this.width*modifier) - (this.side*modifier), y0 + (this.height*modifier));
            this.ctx.lineTo(x0, y0 + ((this.height / 2)*modifier));
            if (highlight == true) {
            }
            if (fillColor && highlight == false) {
                this.ctx.fillStyle = fillColor;
                this.ctx.fill();
            }
            this.ctx.closePath();
            this.ctx.stroke();
        }else {
            this.ctx.beginPath();
            this.ctx.moveTo(x0 + this.width - this.side, y0);
            this.ctx.lineTo(x0 + this.side, y0);
            this.ctx.lineTo(x0 + this.width, y0 + (this.height / 2));
            this.ctx.lineTo(x0 + this.side, y0 + this.height);
            this.ctx.lineTo(x0 + this.width - this.side, y0 + this.height);
            this.ctx.lineTo(x0, y0 + (this.height / 2));
            if (highlight == true) {
            }
            if (fillColor && highlight == false) {
                this.ctx.fillStyle = fillColor;
                this.ctx.fill();
            }
            this.ctx.closePath();
            this.ctx.stroke();
        }
        if (hexText) {
            this.ctx.font = "5px";
            this.ctx.fillStyle = "#000";
            this.ctx.fillText(hexText, x0 + (this.width / 2) - (this.width / 4), y0 + (this.height - 5));
        }
    }
    hex.biome = function(e, m) {
        if (e < 0.1){ return "#0077be"}
        if (e < 0.12){ return "#FFEBCD"}

        if (e > 0.8) {
            if (m < 0.1){ return "#FFFF80"}
            if (m < 0.2){ return "#471C01" }
            if (m < 0.5){ return "#6a6c3b" }
            return "#FFFFFF";
        }

        if (e > 0.6) {
            if (m < 0.33){ return "#E0E080" }
            if (m < 0.66){ return "#F0F080" }
            return "#c4b884";
        }

        if (e > 0.3) {
            if (m < 0.16){ return "#E0E080" }
            if (m < 0.50){ return "#B0F080" }
            if (m < 0.83){ return "#60E080"}
            return "#20E0C0";
        }

        if (m < 0.16){ return "#F0F080"}
        if (m < 0.33){ return "#E0E080"}
        if (m < 0.66){ return "#60F080"}

        return "#20FFA0";

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
        var offSet = hex.canvas.getBoundingClientRect();
        mouseX -= offSet.left;
        mouseY -= offSet.top;

        var column = Math.floor((mouseX) / hex.side);
        var row = Math.floor(column % 2 == 0 ? Math.floor((mouseY) / hex.height) : Math.floor(((mouseY + (hex.height * 0.5)) / hex.height)) - 1);

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
            $('#tile_info').text(tile);
        }
        if (tile.row < hex.game_info.rows && tile.row >= 0 && tile.col < hex.game_info.columns && tile.col >= 0) {
            //console.log(tile);
            for (var row = 0; row < hex.hexes.length; row++) {
                for (var column = 0; column < hex.hexes[row].length; column++) {
                    currentHex = {"row": hex.hexes[row][column].row, "col": hex.hexes[row][column].column};
                    if (JSON.stringify(currentHex) == JSON.stringify(tile)){
                        hex.turn_handler(hex.hexes[row][column]);
                        if (GLOBALS.DEBUG == true) {
                            str = "";
                            for (var key in hex.hexes[row][column]) {
                                str += "<b>"+ key + ":</b> " + hex.hexes[row][column][key] + "<br>";
                            }
                            $('#tile_info').html(str);
                            console.log(hex.hexes[row][column]);
                        }
                    }
                }
            }
            this.draw();
        } else {
            console.log("Click out of range");
        }

    };

    hex.turn_handler = function(tile){
        if (hex.game_info.turn_phase == 'unit_placement' && hex.game_info.turn_player == tile.owner){
            console.log("unit placement");
            hex.actions.push({
                "type": "unit_placement",
                "amount": 1,
                "tile": tile
            });
            hex.tiles_changed.forEach(function(tile_search, index) {
                if (tile_search.column == tile.column && tile_search.row == tile.row){
                    hex.tiles_changed.splice(index, 1);
                }
            });
            tile.units += 1;
            hex.tiles_changed.push(tile);
        }else{
            console.log("not", tile);
            for (var row = 0; row < hex.hexes.length; row++) {
                for (var column = 0; column < hex.hexes[row].length; column++) {
                    if (hex.hexes[row][column].row == tile.row && hex.hexes[row][column].column == tile.column){
                        hex.highlight('attack', row, column);
                    }
                }
            }


        }
    };
    hex.highlight = function(phase, row, column){
        if (phase == 'attack'){
            hex.hexes[row][column].highlighted = hex.hexes[row][column].highlighted ? false : true;
            cube_coords = hex.toCubeCoord(hex.hexes[row][column].column, hex.hexes[row][column].row);
            neighors = hex.getNeighbors(cube_coords.x, cube_coords.y, cube_coords.z);
            for (var i = 0; i < neighors.length; i++){
                coords = hex.toOffsetCoord(neighors[i].x, neighors[i].y, neighors[i].z)
                console.log("coords", coords);
                hex.hexes[coords.r][coords.q].highlighted = hex.hexes[coords.r][coords.q].highlighted ? false : true;
                if (hex.hexes[coords.r][coords.q].highlighted == true){
                    hex.hexes[coords.r][coords.q].highlight_color = "#f44242";
                }
            }
            this.draw();
        }
    };

    hex.clearMap = function(){
        this.hexes = [];
        this.defineHexGrid(this.rows, this.cols);
        this.draw()
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