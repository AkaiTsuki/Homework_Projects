package secondary;

import java.io.DataInput;
import java.io.DataOutput;
import java.io.IOException;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.io.FloatWritable;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.NullWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.io.WritableComparable;
import org.apache.hadoop.io.WritableComparator;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Partitioner;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.util.GenericOptionsParser;
import org.apache.hadoop.fs.Path;

import au.com.bytecode.opencsv.CSVParser;

public class AirlineDelayMapReducer {

	private static final int YEAR = 0;
	private static final int MONTH = 2;
	private static final int AIRLINE_ID = 7;
	private static final int ARR_DELAY_MINUTES = 37;
	private static final int CANCELLED = 41;
	private static final int DIVERTED = 43;

	public static class AirlineKey implements WritableComparable<AirlineKey> {
		private IntWritable airlineId;
		private IntWritable month;

		public AirlineKey() {
			airlineId = new IntWritable();
			month = new IntWritable();
		}

		@Override
		public void readFields(DataInput in) throws IOException {
			airlineId.readFields(in);
			month.readFields(in);
		}

		@Override
		public void write(DataOutput out) throws IOException {
			airlineId.write(out);
			month.write(out);
		}

		@Override
		public int compareTo(AirlineKey key) {
			int cmp = airlineId.compareTo(key.getAirlineId());
			if (cmp != 0)
				return cmp;
			return month.compareTo(key.getMonth());
		}

		public void set(int id, int month) {
			airlineId.set(id);
			this.month.set(month);
		}

		public IntWritable getAirlineId() {
			return airlineId;
		}

		public void setAirlineId(IntWritable airlineId) {
			this.airlineId = airlineId;
		}

		public IntWritable getMonth() {
			return month;
		}

		public void setMonth(IntWritable month) {
			this.month = month;
		}

		@Override
		public int hashCode() {
			final int prime = 31;
			int result = 1;
			result = prime * result
					+ ((airlineId == null) ? 0 : airlineId.hashCode());
			result = prime * result + ((month == null) ? 0 : month.hashCode());
			return result;
		}

		@Override
		public boolean equals(Object obj) {
			if (this == obj)
				return true;
			if (obj == null)
				return false;
			if (getClass() != obj.getClass())
				return false;
			AirlineKey other = (AirlineKey) obj;
			if (airlineId == null) {
				if (other.airlineId != null)
					return false;
			} else if (!airlineId.equals(other.airlineId))
				return false;
			if (month == null) {
				if (other.month != null)
					return false;
			} else if (!month.equals(other.month))
				return false;
			return true;
		}

	}

	public static class MonthPartitioner extends
			Partitioner<AirlineKey, FloatWritable> {

		@Override
		public int getPartition(AirlineKey key, FloatWritable val,
				int numOfReducers) {
			return key.getAirlineId().get() % numOfReducers;
		}
	}

	public static class GroupComparator extends WritableComparator {
		protected GroupComparator() {
			super(AirlineKey.class, true);
		}

		@Override
		public int compare(WritableComparable a, WritableComparable b) {
			AirlineKey key1 = (AirlineKey) a;
			AirlineKey key2 = (AirlineKey) b;
			return key1.getAirlineId().compareTo(key2.getAirlineId());
		}

	}

	public static class AirlineMapper extends
			Mapper<Object, Text, AirlineKey, FloatWritable> {
		private AirlineKey airlineKey = new AirlineKey();
		private FloatWritable airlineValue = new FloatWritable();

		public void map(Object key, Text value, Context context)
				throws IOException, InterruptedException {
			CSVParser parser = new CSVParser();
			String[] entry = parser.parseLine(value.toString());
			if (isValidFlight(entry)) {
				airlineKey.set(Integer.parseInt(entry[AIRLINE_ID]),
						Integer.parseInt(entry[MONTH]));
				airlineValue.set(Float.parseFloat(entry[ARR_DELAY_MINUTES]));
				context.write(airlineKey, airlineValue);
			}
		}

		private boolean isValidFlight(String[] entry) {
			float cancelled = Float.parseFloat(entry[CANCELLED]);
			float diverted = Float.parseFloat(entry[DIVERTED]);
			int year = Integer.parseInt(entry[YEAR]);

			return year == 2008 && cancelled == 0.0 && entry[ARR_DELAY_MINUTES].length() > 0;
		}
	}

	public static class AirlineReducer extends
			Reducer<AirlineKey, FloatWritable, NullWritable, Text> {

		private Text delays = new Text();

		public void reduce(AirlineKey key, Iterable<FloatWritable> values,
				Context context) throws IOException, InterruptedException {

			float sum = 0;
			int count = 0;
			int currentMonth = -1;
			int[] averages = new int[12];

			for (FloatWritable v : values) {
				int month = key.getMonth().get();
				if (currentMonth == -1)
					currentMonth = month;
				float delay = v.get();

				if (month != currentMonth) {
					int avg = 0;
					if (count != 0) {
						avg = (int) Math.ceil((sum / count));
					}
					averages[currentMonth - 1] = avg;
					sum = delay;
					count = 1;
					currentMonth = month;
				} else {
					sum += delay;
					count += 1;
				}
			}
			averages[currentMonth - 1] = (int) Math.ceil((sum / count));
			delays.set(key.getAirlineId().get() + ", "
					+ getDelayString(averages));
			context.write(NullWritable.get(), delays);
		}

		private String getDelayString(int[] averages) {
			String s = "";
			for (int i = 0; i < averages.length; i++) {
				if (s.length() > 0) {
					s += ", ";
				}
				s += "(" + (i + 1) + ", " + averages[i] + ")";
			}
			return s;
		}
	}

	public static void main(String[] args) throws Exception {
		Configuration conf = new Configuration();
		String[] otherArgs = new GenericOptionsParser(conf, args)
				.getRemainingArgs();
		if (otherArgs.length != 2) {
			System.err.println("Usage: Flight Secondary Sort <in> <out>");
			System.exit(2);
		}
		Job job = new Job(conf, "Flight Secondary Sort");

		job.setJarByClass(AirlineDelayMapReducer.class);
		job.setMapperClass(AirlineMapper.class);

		job.setPartitionerClass(MonthPartitioner.class);
		job.setReducerClass(AirlineReducer.class);
		// Set number of reduce tasks
		job.setNumReduceTasks(10);
		job.setGroupingComparatorClass(GroupComparator.class);

		job.setMapOutputKeyClass(AirlineKey.class);
		job.setMapOutputValueClass(FloatWritable.class);
		job.setOutputKeyClass(NullWritable.class);
		job.setOutputValueClass(Text.class);

		FileInputFormat.addInputPath(job, new Path(otherArgs[0]));
		FileOutputFormat.setOutputPath(job, new Path(otherArgs[1]));
		job.waitForCompletion(true);
	}

}
