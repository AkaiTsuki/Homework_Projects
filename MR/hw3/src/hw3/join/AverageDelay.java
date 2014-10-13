package hw3.join;

import java.io.*;

public class AverageDelay {

	public static void main(String[] args) throws Exception {
		// TODO Auto-generated method stub
		BufferedReader bf = new BufferedReader(new FileReader("output/part-r-00000"));
		String line = null;
		double sum = 0;
		int count = 0;
		while((line=bf.readLine()) != null){
			count ++;
			sum += Float.parseFloat(line.trim());
		}
		System.out.println(sum/count);
	}

}
