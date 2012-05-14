/*

Author: Anthony Lazzaro (www.tonyzaro.com) 

Based upon 'tree' by Evelyn Eastmond, licensed under Creative Commons Attribution-Share Alike 3.0 and GNU GPL license.
Work: http://openprocessing.org/visuals/?visualID=1249	
License: 
http://creativecommons.org/licenses/by-sa/3.0/
http://creativecommons.org/licenses/GPL/2.0/
*/

//color bg = color(random(100,150),random(100,150),random(100,150)); //background color
//color branchColor = color ( random(0,255),random(0,255),random(0,255),255 );//branch color
//color leafColor = color ( random(0,255),random(0,255),random(0,255) );//leaf color 

color bg;
color branchColor;
color leafColor;

void createColorPalette(){
 bg = color(bgColorArray[0],bgColorArray[1],bgColorArray[2]);          //background color	
 branchColor = color ( branchColorArray[0],branchColorArray[1],branchColorArray[2],255 );   //branch color
 leafColor = color ( leafColorArray[0],leafColorArray[1],leafColorArray[2]);                //leaf color 

}

void setup() {
  size(450, 450);
  noLoop();
}

void draw(){
	createColorPalette();
 	background(bg);
	drawTree(11);
	drawTree(6);
	drawTree(2);
}

/*
void mousePressed(){
   redraw();
}
*/

 
void drawTree(int maxdepth){
    
    translate(225,300);	
    strokeWeight(maxdepth*1.5);
    stroke(branchColor);
    line(0,100,0,0);
    branch(maxdepth);
}
   
 
void branch(int depth){
  pushMatrix();                    // store the old state
  rotate(radians(random(0,45)));   // rotate
  subBranch(depth);                // and draw one branch
  popMatrix();                     // go back to old state
  rotate(radians(random(-45,-0))); // rotate the other way
  subBranch(depth);                // and draw another branch
}
 
void subBranch(int depth) {
  scale(0.8);
  int len = (int) random(0,100);
  translate(0,-len);
  strokeWeight(depth*1.5);
  line(0,len,0,0);
  fill(leafColor);
  if(depth == 0) {ellipse(0,0,random(190,200),random(80,100));}
  if(depth > 0) branch(depth-1);
}


