float theta;  
int degreelvl = 80; 
color my_color = color(255,0,0);
color lasagna = color(155,75,31);
//http://0.tqn.com/d/kidscooking/1/0/Y/9/-/-/vegetablelasagnabig.jpg

void setup() {
  size(450, 450);
  smooth();
  frameRate(60);
}

void draw() {

  background(255);

  stroke(lasagna);
  // Let's pick an angle 0 to 90 degrees based on the mouse position
  //float a = (mouseX / (float) width) * 90f;
  /*
  if(degreelvl > 90){
 	 degreelvl = 0;
  }
  else{
  degreelvl++;
  }
  */
  // Convert it to radians
  theta = radians(degreelvl);
  // Start the tree from the bottom of the screen
  translate(width/2,height);
  //rotate(PI/3.0);
  // Draw a line 120 pixels
  line(0,0,0,-120);
  // Move to the end of that line
  translate(0,-120);
  // Start the recursive branching!
  branch(120);

}

void branch(float h) {
  // Each branch will be 2/3rds the size of the previous one
  h *= 0.66;
  //h *= random (0.22,0.66);
  // All recursive functions must have an exit condition!!!!
  // Here, ours is when the length of the branch is 2 pixels or less
  if (h > 2) {
    pushMatrix();    // Save the current state of transformation (i.e. where are we now)
    rotate(theta);   // Rotate by theta
    line(0, 0, 0, -h);  // Draw the branch
    translate(0, -h); // Move to the end of the branch
    branch(h);       // Ok, now call myself to draw two new branches!!
    popMatrix();     // Whenever we get back here, we "pop" in order to restore the previous matrix state
    
    // Repeat the same thing, only branch off to the "left" this time!
    pushMatrix();
    rotate(-theta);
    line(0, 0, 0, -h);
    translate(0, -h);
    branch(h);
    popMatrix();
  }
}