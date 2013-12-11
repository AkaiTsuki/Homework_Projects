import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class DTW {

	private int[] X;
	private int[] Y;
	private int[][] D;
	private List<Step> paths;
	
	class Step{
		public int x;
		public int y;
		
		public Step(int x,int y){
			this.x = x;
			this.y = y;
		}

		/* (non-Javadoc)
		 * @see java.lang.Object#toString()
		 */
		@Override
		public String toString() {
			return "Step [x=" + x + ", y=" + y + "]";
		}
		
		
	}

	public DTW(int[] X, int[] Y) {
		this.X = X;
		this.Y = Y;
		D = new int[X.length][Y.length];

		for (int i = 0; i < X.length; i++)
			for (int j = 0; j < Y.length; j++)
				D[i][j] = -1;
		D[0][0] = this.costByIndex(0, 0);
		this.initD();
		paths = new ArrayList<Step>();
		paths.add(new Step(19,19));
	}

	public void initD() {
		for (int i = 1; i < Y.length; i++) {
			D[0][i] = D[0][i - 1] + this.costByIndex(0, i);
		}

		for (int j = 1; j < X.length; j++) {
			D[j][0] = D[j - 1][0] + this.costByIndex(j, 0);
		}
	}
	
	public int L1Norm(){
		int norm = 0;
		for(int i=0;i<X.length;i++){
			norm += this.costByIndex(i, i);
		}
		return norm;
	}

	public int calculateDTW() {
		return calculateDTW(19, 19);
	}

	public int calculateDTW(int x, int y) {
		if (D[x][y] != -1){
			//System.out.println("From :"+x+" "+y);
			return D[x][y];
		}
			

		else {
			
			int val1 = calculateDTW(x - 1, y);
			int val2 = calculateDTW(x, y - 1);
			int val3 = calculateDTW(x - 1, y - 1);

			int min = this.findMin(val1, val2, val3);
			D[x][y] = min + this.costByIndex(x, y);
			return D[x][y];
		}
	}
	
	public void printPath(int x,int y){
		
		while(x-1>=0 && y-1>=0){
			int fromX = x-1;
			int fromY = y;
			
			int c1 = D[x-1][y];
			int c2 = D[x][y-1];
			int c3 = D[x-1][y-1];
			
			int min = c1;
			
			if(min>c2){
				min = c2;
				fromX = x;
				fromY = y-1;
			}
			
			if(min>c3){
				min = c3;
				fromX = x-1;
				fromY = y-1;
			}
			
			Step step = new Step(fromX,fromY);
			this.paths.add(step);
			//System.out.println(step);
			x = fromX;
			y = fromY;
			
		}	
		paths.add(new Step(0,0));
		//System.out.println(paths);
	}
	
	public void check(int expect, List<Step> path){
		int cost = 0;
		for(int i=path.size()-1;i>=0;i--){
			Step s = path.get(i);
			int x =s.x;
			int y =s.y;
			System.out.println("Step: "+x+" "+y);
			cost += this.costByIndex(x, y);
		}
		System.out.println(expect==cost);
	}

	private int findMin(int x, int y, int z) {
		int val = x;
		if (y < val)
			val = y;
		if (z < val)
			val = z;
		return val;
	}

	public int costByIndex(int x, int y) {
		return Math.abs(this.X[x] - this.Y[y]);
	}

	/*
	 * public static int cost(int x, int y) { return Math.abs(x - y); }
	 * 
	 * public static int[][] createCostMatrix(int[] X, int[] Y) { int M =
	 * X.length; int N = Y.length; int[][] costMatrix = new int[M][N];
	 * 
	 * // Set all element to -1 for (int i = 0; i < M; i++) for (int j = 0; j <
	 * N; j++) costMatrix[i][j] = -1;
	 * 
	 * // Calculate cost for (int i = 0; i < M; i++) for (int j = 0; j < N; j++)
	 * costMatrix[i][j] = cost(X[i], Y[j]);
	 * 
	 * return costMatrix; }
	 */
	public static void printMatrix(int[][] matrix) {
		for (int i = 0; i < matrix.length; i++) {
			for (int j = 0; j < matrix[0].length; j++) {
				int val = matrix[i][j];
				if (val >= 100)
					System.out.print(val + " ");
				else if (val >= 10)
					System.out.print(val + "  ");
				else
					System.out.print(val + "   ");
			}
			System.out.println();
		}

	}

	/**
	 * @return the x
	 */
	public int[] getX() {
		return X;
	}

	/**
	 * @param x
	 *            the x to set
	 */
	public void setX(int[] x) {
		X = x;
	}

	/**
	 * @return the y
	 */
	public int[] getY() {
		return Y;
	}

	/**
	 * @param y
	 *            the y to set
	 */
	public void setY(int[] y) {
		Y = y;
	}

	/**
	 * @return the d
	 */
	public int[][] getD() {
		return D;
	}

	/**
	 * @param d
	 *            the d to set
	 */
	public void setD(int[][] d) {
		D = d;
	}
	
	

	/**
	 * @return the paths
	 */
	public List<Step> getPaths() {
		return paths;
	}

	/**
	 * @param paths the paths to set
	 */
	public void setPaths(List<Step> paths) {
		this.paths = paths;
	}

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		int[] X = { 71, 73, 80, 80, 80, 78, 76, 75, 73, 71, 71, 71, 73, 75, 76,
				76, 68, 76, 76, 75 };
		int[] Y = { 69, 69, 73, 79, 80, 79, 78, 76, 73, 72, 71, 70, 70, 69, 69,
				69, 71, 73, 75, 76 };

		System.out.println(Arrays.toString(X));
		System.out.println(Arrays.toString(Y));

		DTW dtw = new DTW(X, Y);
		System.out.println("L1 Norm: "+dtw.L1Norm());
		//DTW.printMatrix(dtw.getD());
		int r = dtw.calculateDTW();
		DTW.printMatrix(dtw.getD());
		System.out.println("Result is " + r);
		dtw.printPath(19, 19);
		
		dtw.check(25, dtw.getPaths());
	}

}
