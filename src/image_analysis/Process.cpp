

#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <assert.h>
#include <ctype.h>
#include <stdlib.h>
#include <algorithm>
#include <iostream>
#include <stdlib.h>
#include <getopt.h>
#include <vector>
#include "linreg.h"
#include <opencv/cv.h>
#include <opencv/highgui.h>

using namespace cv;
using namespace std;

#define MAXN 5000
#define MINF 0.5
#define MAXF 2
#define MINA 50
#define MINDIST 20
#define RIGHTANGLE 1.5707963267949
#define GRIDTIGHT 0.5
#define MARGIN 0.1

struct Shape {
  double x;
  double y;
  double Ox;
  double Oy;
  double area;
  double circ;
  int xm;
  int ym;
  int good;
  double estArea;
  vector<Point> contour;
};


int PrintColumns = 0;
int Debug = 0;
int Threshold = -1;
int BackgroundWidth = -1;
double Dist[MAXN];
double Angle[MAXN];
double MaxX, MaxY, MinX, MinY;
double LowX, HighX, LowY, HighY;
//int n;
double SetDist = -1;
int Rows = 16;
int Columns = 24;

vector< vector<int> > Grid;
vector<Shape> Shapes;

void
ParseImage( char const* imagename, Mat& img )
{
    img = imread(imagename);
    if( !img.data ) // check if the image has been loaded properly
    {
      cerr << "Can't open file " << imagename << endl;
      exit(-1);
    }
    
    Mat bin = Mat( img.cols, img.rows, CV_8UC1 );
    cvtColor( img, bin, CV_RGB2GRAY );

    bitwise_xor(bin, 255, bin );
    Mat el5 = getStructuringElement( MORPH_ELLIPSE, Size(15, 15) );
    Mat back = Mat( img.cols, img.rows, CV_8UC1 );

    if( BackgroundWidth < 0 )
      BackgroundWidth = min( img.rows / (Rows+1), img.cols / (Columns+1));

    if( (BackgroundWidth % 2) == 0 )
      BackgroundWidth++;

    //    cerr << "Background Width = " << BackgroundWidth << endl;
    if( false )
    {
      medianBlur( bin, back, BackgroundWidth );
    } else
    {
      Mat el = getStructuringElement( MORPH_ELLIPSE,
				      Size(BackgroundWidth, BackgroundWidth) );
      morphologyEx( bin, back, CV_MOP_OPEN, el );
    }
    imwrite("processBack.jpg", back );
    subtract( bin, back, bin );
    imwrite("processBackSub.jpg", bin );
    

    if( Threshold >= 0 )
      threshold( bin, bin,Threshold,256, CV_THRESH_BINARY );
    else
      threshold( bin, bin,128,256, CV_THRESH_BINARY | CV_THRESH_OTSU );

    erode( bin, bin, el5 );
    dilate( bin, bin, el5 );
    imwrite("processBin.jpg", bin );

    vector<vector<Point> > contours;
    findContours( bin, contours, CV_RETR_TREE, CV_CHAIN_APPROX_SIMPLE );

    MinX = 100000;
    MinY = 100000;
    MaxX = 0;
    MaxY = 0;
    
    vector<vector<Point> >::iterator i;
    for( i = contours.begin(); i != contours.end(); i++ )
    {
      Shape S;
      Mat C(*i);
      S.contour = *i;
      S.area = contourArea( C );
      RotatedRect rect;
      if(  C.rows < 6 )
      {
	Rect Rrect = boundingRect( C );

	rect = RotatedRect( Point2f(Rrect.x+Rrect.width/2, Rrect.y+Rrect.height/2 ), Rrect.size(), 0.0 );
      } else
	rect = fitEllipse( C );
      S.Ox = S.x = rect.center.x;
      S.Oy = S.y = rect.center.y;
      double perim = arcLength( C, true );
      S.circ = perim*perim/(4*3.14*S.area);
      if( S.circ >= MINF && S.circ <= MAXF && S.area >= MINA )
      {
	//	cerr << " x =" << S.x << " y = " << S.y << " circ = " << S.circ << " area = " << S.area << endl;
	MaxX = max( MaxX, S.x );
	MaxY = max( MaxY, S.y );
	MinX = min( MinX, S.x );
	MinY = min( MinY, S.y );
	Shapes.push_back( S );
	//	circle( img, rect.center, rect.size.height/2, Scalar(0,0,255), 2 );
      }
    }

    drawContours( img, contours, -1, Scalar(255,255,255) );

    double dX = MaxX - MinX;
    LowX = MinX + MARGIN*dX;
    HighX = MaxX - MARGIN*dX;
    double dY = MaxY - MinY;
    LowY = MinY + MARGIN*dY;
    HighY = MaxY - MARGIN*dY;
    //    cerr << "MinX = " << MinX << " MinY = " << MinY
    //	 << " MaxX = " << MaxX << " MaxY = " << MaxY << endl;
    //    cerr << "LowX = " << LowX << " LowY = " << LowY
    //	 << " HighX = " << HighX << " HighY = " << HighY << endl;
}

double
DistSq( int i, int j )
{
  double dx = (Shapes[i].x - Shapes[j].x);
  double dy = (Shapes[i].y - Shapes[j].y);
  
  return dx*dx+dy*dy;
}

double
FindAngle( int i, int j )
{
  double dx = (Shapes[i].x - Shapes[j].x);
  double dy = (Shapes[i].y - Shapes[j].y); 
  return atan( dy/dx );
}


void
AddHist(int i, int& N)
{
  int closest = -1;
  double d = 100000.0;
  
  for( int j = 0; j < Shapes.size(); j++ )
    if( j != i )
    {
      double dj = DistSq( i, j );
      if( dj > MINDIST && dj < d )
      {
	closest = j;
	d = dj;
      }
    }
  d = sqrt(d);
  double a = FindAngle( i, closest );

  if( a > RIGHTANGLE/2 )
    a -= RIGHTANGLE;
  if( a < -RIGHTANGLE/2 )
    a += RIGHTANGLE;

  if( SetDist < 0 || fabs( d - SetDist ) < 5 )
  {
    Dist[N] = d;
    Angle[N] = a;
    N++;
  }
}


double Ox, Oy, GridDist;
double GridAngle = 0.0;

void
RotatePoints( double A )
{
  GridAngle -= A;
  
  double sA = sin(A);
  double cA = cos(A);
  int i;
  for( i = 0; i < Shapes.size(); i++ )
  {
    double nX = Shapes[i].x*cA - Shapes[i].y*sA;
    double nY = Shapes[i].x*sA + Shapes[i].y*cA;
    Shapes[i].x = nX;
    Shapes[i].y = nY;
  }
}

double
Median( vector<double>& O )
{
  int n = O.size();
  nth_element( O.begin(), O.begin()+n/2, O.end() );
  return O[n/2];
}

double
FindOffsetX( double d )
{
  vector<double> O(Shapes.size());
  int i;
  for( i = 0; i < Shapes.size(); i++ )
  {
    int k = (int) Shapes[i].x/d;
    O[i] = Shapes[i].x - k*d;
  }
  return Median( O );
}


double
FindOffsetY( double d )
{
  vector<double> O(Shapes.size());
  int i;
  for( i = 0; i < Shapes.size(); i++ )
  {
    int k = (int) Shapes[i].y/d;
    O[i] = Shapes[i].y - k*d;
  }
  return Median( O );
}

void
Quantize(double D, double A, int MinX, int MinY)
{
  static int Iter = 1;
  RotatePoints(-A);

  int Goods = 0;
  
  Ox = FindOffsetX( D );
  Oy = FindOffsetY( D );
  while( Ox < MinX )
    Ox += D;
  while( Oy < MinY )
    Oy += D;
  
  GridDist = D;
  //  if( Debug )
  //  cerr << "Offset = " << Ox << " " << Oy << endl;

  for( int i = 0; i < Shapes.size(); i++ )
  {
    double Xn = (Shapes[i].x - Ox)/D;
    double Yn = (Shapes[i].y - Oy)/D;
    Shapes[i].xm = (int)(Xn+0.5);
    Shapes[i].ym = (int)(Yn+0.5);
    double dX = Xn - Shapes[i].xm;
    double dY = Yn - Shapes[i].ym;
    double d = sqrt(dX*dX + dY*dY);
#ifdef notdef
    cerr << " " << i
	 << " " << Shapes[i].x
	 << " " << Shapes[i].y
	 << " " << Shapes[i].xm 
	 << " " << Shapes[i].ym
	 << " " << d 
	 << endl;
#endif
    if( (fabs(dX) < GRIDTIGHT && fabs(dY) < GRIDTIGHT ) )
    {
      Goods ++;
      Shapes[i].good = Iter;
    } else
      Shapes[i].good = 0;
  }
  Iter++;
  //  cerr << "Goods = " << Goods << endl;
}

int
Score( int r0, int c0 )
{
  int S = 0;
  int i;
  int Seen[Rows][Columns];
  for( int r = 0; r < Rows; r++ )
    for( int c = 0; c < Columns; c++ )
      Seen[r][c] = 0;
    
  for( i = 0 ; i < Shapes.size(); i++ )
  {
    int r = Shapes[i].ym - r0;
    int c = Shapes[i].xm - c0;
    if( Shapes[i].good > 0 && c >= 0 && c < Columns && r >= 0  && r < Rows )
      if( Seen[r][c] == 0 )
      {
	Seen[r][c]++;
	S++;
      }
  }
  return S;
}

int
CheckNeighbor( int r, int c )
{
  if( r < 0 || r == Rows )
    return 0;
  if( c < 0 || c == Columns )
    return 0;
  return Grid[r][c] >= 0 ? 1 : 0;
}

int
Neighbors4( int r, int c )
{
  int n = 0;
  n += CheckNeighbor( r-1, c );
  n += CheckNeighbor( r+1, c );
  n += CheckNeighbor( r, c+1 );
  n += CheckNeighbor( r, c-1 );
  return n;
}

int
Neighbors8( int r, int c )
{
  int n = 2*Neighbors4( r, c );
  n += CheckNeighbor( r-1, c-1 );
  n += CheckNeighbor( r+1, c+1 );
  n += CheckNeighbor( r-1, c+1 );
  n += CheckNeighbor( r+1, c-1 );
  return n;
}

void
SetGrid( int r0, int c0, double D )
{
  int i;
  for( int r = 0; r < Rows; r++ )
    for( int c = 0; c < Columns; c++ )
    {
      Grid[r][c] = -1;
    }
    
  for( i = 0 ; i < Shapes.size(); i++ )
  {
    int r = Shapes[i].ym - r0;
    int c = Shapes[i].xm - c0;
    if( Shapes[i].good && c >= 0 && c < Columns && r >= 0  && r < Rows )
    {
      if( Grid[r][c] < 0 || Shapes[i].area > Shapes[Grid[r][c]].area )
        Grid[r][c] = i;
    }
  }
  if( Debug )
    cerr << "Set c0 = " << c0 << " r0 = " << r0 << endl;
  Ox += D* c0;
  Oy += D* r0;
}

void
EstimateExpectedSizes()
{
  vector<vector<double> > Sizes8(13);

  for( int r = 0; r < Rows; r++ )
      for( int c = 0; c < Columns; c++ )
	if( Grid[r][c] >= 0 )
	{
	  int n8 = Neighbors8( r, c );
	  Sizes8[n8].push_back( Shapes[Grid[r][c]].area );
	}

  LinearRegression Reg8;
  
  for( int i = 0; i < 13; i++ )
  {
    int n = Sizes8[i].size();
    if( n > 2 )
    {
      int n2 = n/2;
      nth_element( Sizes8[i].begin(), Sizes8[i].begin()+n2, Sizes8[i].end() );
      for( int j = 0; j < n; j++ )
	Reg8.addXY( i, Sizes8[i][n2]);
    }
  }

  for( int r = 0; r < Rows; r++ )
      for( int c = 0; c < Columns; c++ )
	if( Grid[r][c] >= 0 )
	{
	  int n8 = Neighbors8( r, c );
	  Shapes[Grid[r][c]].estArea = Reg8.estimateY(n8);
	}
}

Point
ImageGridPoint( double x, double y )
{
  double sA = sin(GridAngle);
  double cA = cos(GridAngle);

  return Point( x*cA - y*sA, x*sA + y*cA );
}

Point
ImageGridCenter( int r, int c )
{
  return ImageGridPoint( Ox+c*GridDist, Oy+r*GridDist );
}

void
ImageGrid( Mat& img )
{
  Scalar eColor( 0,0,0 );
  Scalar cColor( 0,0,255 );

  //  Point Orig( Ox, Oy );
  //  circle( img, Orig, 8, Scalar(200,200,255), -1 );
  //  circle( img, ImageGridPoint(Ox,Oy), 8, Scalar(255,0,255), -1 );

  //  line( img, ImageGridCenter( 0,0), ImageGridCenter( 0, Columns-1 ), Scalar(255,0,255), 2 );
  //  line( img, ImageGridCenter( 0,0), ImageGridCenter( Rows-1, 0 ), Scalar(255,0,255), 2 );
    
  if( Debug )
    cerr << "Ox = " << Ox << " Oy = " << Oy << endl;
  //  img = Scalar(0,0,0);
  for( int r = 0; r < Rows; r++ )
  {    
    for( int c = 0; c < Columns; c++ )
    {
      Point center = ImageGridCenter( r, c );
      circle( img, center, 2, eColor, 2 );

      if( Grid[r][c] >= 0 )
      {
	Shape& S = Shapes[Grid[r][c]];
	double rad = sqrt(S.estArea / 3.14);
	//	circle( img, center, rad, eColor, 2 );
	circle( img, Point(S.Ox, S.Oy), rad, eColor, 2 );	
	rad = sqrt(S.area / 3.14);
	circle( img, Point(S.Ox, S.Oy), rad, cColor, 2 );	
      }
    }
  }
}


string
ReplaceSubString(string base, string old, string replacement)
{
    size_t index = 0;
    while (true)
    {
        /* Locate the substring to replace. */
        index = base.find(old, index);
        if (index == string::npos) break;

        /* Make the replacement. */
        base.replace(index, old.length(), replacement);

        /* Advance index forward so the next iteration doesn't pick it up as well. */
        index += old.length();
    }

    return base;
}



void
PrintGrid( double D )
{
  double ReScale = (100/D)*(100/D);



  
  std::stringstream ss;
  std::stringstream s_columns;
  std::stringstream s_rows;
  std::stringstream column;
  std::stringstream s_ratio;
  std::stringstream s_center_x;
  std::stringstream s_center_y;
  std::stringstream s_area_scaled;

  
  
  ss << D;
  s_rows << Rows;
  s_columns << Columns;
  
  string j_grid = "{'type': 'yeast_plate', 'columns': " + s_columns.str() + ", 'rows': " + s_rows.str() + ", 'factor': " + ss.str() + ", 'rescale': '(100/D)*(100/D)', 'grid': [";
  
  if( PrintColumns )
    cout << Columns << endl;
  
  for( int r = 0; r < Rows; r++ )
  {
      ss.str("");
      ss << r;
      
      for( int c = 0; c < Columns; c++ )
      {
          column.str("");
          column << c;

          
          if( Grid[r][c] >= 0 )
          {
              double ratio = Shapes[Grid[r][c]].area/Shapes[Grid[r][c]].estArea;
              Point center = ImageGridCenter( r, c );


              //nir code commented out in favor of JSON didn't get JSON API so I coul'd learn basic c++ and avoid importing for now
              
              //cout << (char)('A' + r) << "\t" << c+1
	      //<< "\t" << Shapes[Grid[r][c]].area*ReScale << "\t" << ratio
	      //<< "\t" << center.x << "\t" << center.y
	      //<< endl;

              s_ratio.str("");
              s_ratio << ratio;

              s_center_x.str("");
              s_center_x << center.x;

              s_center_y.str("");
              s_center_y << center.y;

              s_area_scaled.str("");
              s_area_scaled << Shapes[Grid[r][c]].area*ReScale;
              
          
              j_grid += "{'row': " + ss.str() + ",";
              j_grid += " 'column': " + column.str()  + ",";
              j_grid += " 'is_empty': false,";
              j_grid += " 'center_x': " + s_center_x.str()  +",";
              j_grid += " 'center_y': " + s_center_y.str()  +",";
              j_grid += " 'area_scaled': " + s_area_scaled.str()  +",";
              j_grid += " 'ratio': "  + s_ratio.str() + "}, ";
          }
          else
          {
              j_grid += "{'row': " + ss.str() + ",";
              j_grid += " 'column': " + column.str()  + ",";
              j_grid += " 'is_empty': true,";
              j_grid += " 'center_x': 0,";
              j_grid += " 'center_y': 0,";
              j_grid += " 'area_scaled': 0,";
              j_grid += " 'ratio': 0}, ";
          }
      }    
  }

  j_grid = j_grid.substr(0, j_grid.length()-2);

  j_grid += "]}";
  
  //cout << j_grid << endl;
  string b = ReplaceSubString(j_grid, "'", "\"");
  cout << b << endl;
}



int
FindGrid( int& r0, int& c0 )
{
  int mR = 0;
  int mC = 0;
  int mr = 0;
  int mc = 0;
  int i;
  
  for( i = 0 ; i < Shapes.size(); i++ )
  {
    if( Shapes[i].good )
    {
      mC = max( mC, Shapes[i].xm );
      mc = min( mc, Shapes[i].xm );
      mR = max( mR, Shapes[i].ym );
      mr = min( mr, Shapes[i].ym );
    }
  }
  
  //  cerr << mR << " " << mC << endl;
  mC -= Columns - 2;
  mR -= Rows - 2;
  mC = max( mC, 1 );
  mR = max( mR, 1 );
  mc = 0;
  mr = 0;
      
  if( Debug ) cerr << "Row 1 in " << mr << " " << mR << endl;
  if( Debug ) cerr << "Col 1 in " << mc << " " << mC << endl;
  int r, c;
  int Best = -1;
  int Count = 0;
  for( r = mr-1; r <= mR; r++ )
    for( c = mc-1; c <= mC; c++ )
    {
      int S = Score( r, c );
      if( Debug ) cerr << r << " " << c << " " << S << endl;
      if( S >= Best )
      {
	if( S == Best )
  	  Count++;
	else
	  Count = 1;
	Best = S;
	r0 = r;
	c0 = c;
      }
    }
  //  cerr << "Best count = " << Count << endl;
  return Count == 1;
}

int
InMargin( int j )
{
  return ( Shapes[j].x >= LowX && Shapes[j].x <= HighX && Shapes[j].y >= LowY && Shapes[j].y <= HighY );
}

void
FindDistAngle( double& D, double& A )
{
  int N = 0;

  for( int j = 0; j < Shapes.size(); j++ )
    if( Shapes[j].good && InMargin(j) )
       AddHist( j, N );

  if( Debug )
    cerr << "N = " << N << endl;
  nth_element( Dist, Dist+N/2, Dist+N );
  D = Dist[N/2];
  if( Debug )
    cerr << "Median Dist = " << D << endl;
    
  nth_element( Angle, Angle+N/2, Angle+N );
  A = Angle[N/2];
  if( Debug )
    cerr << "Median Angle = " << A << endl;
}


void
InitFirstPoints()
{
    
  for( int j = 0; j < Shapes.size(); j++ )
    Shapes[j].good = 1;
}

void
usage( char* str )
{
  if( str )
    cerr << str << endl << endl;
  cerr << "Usage:\n"
          "Process [options] image\n"
          "\n"
          "options:\n"
          "  -9         96 well plate format\n"
          "  -3         384 well plate format\n"
          "  -1         1354 well format\n"
          "  -D         Display image in a window\n"
          "  -i <file>  Output image to a file\n"
          "  -w <width> Force grid width\n"
          "  -t <thrsh> Force threshold\n"
	  "  -x <x>     Set minimal X coordinate for top-left corner\n"
	  "  -y <y>     Set minimal Y coordinate for top-left corner\n"
          "  -C         Print column number at the beginning of output\n"
          "  -h         Usage\n"
          "\n";
  exit( -1 );
}

int
main(int ac, char** av )
{
  int c;
  char *ImageOutput = NULL;
  int Display = 0;
  int MinX = 0;
  int MinY = 0;
  while( (c = getopt(ac, av, "h139dt:w:Di:B:x:y:C")) != -1 )
  {
    switch( c )
    {
    case 'C':
      PrintColumns = 1;
      break;
    case 'x':
      MinX = atoi(optarg);
      break;
    case 'y':
      MinY = atoi(optarg);
      break;
    case 'w':
      SetDist = atof(optarg);
      break;
    case 'B':
      BackgroundWidth = atof(optarg);
      break;
    case 't':
      Threshold = atoi( optarg );
      break;
    case '9':
      Rows = 8;
      Columns = 12;
      break;
    case '1':
      Rows = 32;
      Columns = 48;
      break;
    case '3':
      Rows = 16;
      Columns = 24;
      break;
    case 'd':
      Debug = 1;
      break;
    case 'D':
      Display = 1;
      break;
    case 'i':
      ImageOutput = strdup( optarg );
      break;
    case 'h':
      usage(NULL);
      break;
    default:
      usage("Unknown option");
    }
  }

  Grid = vector<vector<int> >(Rows, vector<int>(Columns, -1));
  
  Mat Img;
  ParseImage( av[optind], Img );

  double D, A;

  if( Debug )
    cerr << "n = " << Shapes.size() <<endl;

  InitFirstPoints();
  FindDistAngle( D, A ); 
  Quantize(D, A, MinX, MinY);

  int r0;
  int c0;
  int Good = FindGrid( r0, c0 );
  int S = Score( r0, c0 );
  if( Debug )
    cerr << "r0 = " << r0 << " c0 = " << c0 << " S = " << S << " M = " << Shapes.size()-S <<
      " Good = " << Good << endl;
  
  FindDistAngle( D, A ); 
  Quantize(D, A, MinX, MinY);

  Good = FindGrid( r0, c0 );
  S = Score( r0, c0 );
  if( Debug )
    cerr << "r0 = " << r0 << " c0 = " << c0 << " S = " << S << " M = " << Shapes.size()-S <<
      " Good = " << Good << endl;

  if( Good )
  {
    SetGrid( r0, c0, D );
    EstimateExpectedSizes();
    PrintGrid( D );
    if( Display || ImageOutput != NULL )
      ImageGrid( Img );
    if( Display )
    {
       namedWindow("Grid", CV_WINDOW_NORMAL | CV_WINDOW_FREERATIO | CV_GUI_EXPANDED );
        imshow("Grid", Img);
	waitKey();
    }
    if( ImageOutput != NULL )
      imwrite( ImageOutput, Img );
  } else
    cerr << "Cannot identify grid automatically" << endl;
  
  exit( Good ? 0 : -1 );
}
