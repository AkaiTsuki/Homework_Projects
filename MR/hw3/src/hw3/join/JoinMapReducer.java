package hw3.join;

import java.io.DataInput;
import java.io.DataOutput;
import java.io.IOException;
import java.util.LinkedList;
import java.util.List;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.BooleanWritable;
import org.apache.hadoop.io.DoubleWritable;
import org.apache.hadoop.io.FloatWritable;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.NullWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.io.WritableComparable;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.util.GenericOptionsParser;

import au.com.bytecode.opencsv.CSVParser;

public class JoinMapReducer {

	private static final int YEAR = 0;
	private static final int MONTH = 2;
	private static final int FLIGHT_DATE = 5;
	private static final int ORIGIN = 11;
	private static final int DEST = 17;
	private static final int ARR_TIME = 35;
	private static final int DEP_TIME = 24;
	private static final int ARR_DELAY_MINUTES = 37;
	private static final int CANCELLED = 41;
	private static final int DIVERTED = 43;

	public static class StopKey implements WritableComparable<StopKey> {

		private Text stop;
		private Text date;

		public StopKey() {
			stop = new Text();
			date = new Text();
		}

		public StopKey(String stop, String date) {
			this.stop = new Text(stop);
			this.date = new Text(date);
		}

		@Override
		public void readFields(DataInput in) throws IOException {
			stop.readFields(in);
			date.readFields(in);
		}

		@Override
		public void write(DataOutput out) throws IOException {
			stop.write(out);
			date.write(out);
		}

		@Override
		public int compareTo(StopKey stopKey) {
			int cmp = this.stop.compareTo(stopKey.getStop());
			if (cmp != 0)
				return cmp;
			return this.date.compareTo(stopKey.getDate());
		}

		public Text getStop() {
			return stop;
		}

		public void setStop(Text stop) {
			this.stop = stop;
		}

		public Text getDate() {
			return date;
		}

		public void setDate(Text date) {
			this.date = date;
		}

		@Override
		public int hashCode() {
			final int prime = 31;
			int result = 1;
			result = prime * result + ((date == null) ? 0 : date.hashCode());
			result = prime * result + ((stop == null) ? 0 : stop.hashCode());
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
			StopKey other = (StopKey) obj;
			if (date == null) {
				if (other.date != null)
					return false;
			} else if (!date.equals(other.date))
				return false;
			if (stop == null) {
				if (other.stop != null)
					return false;
			} else if (!stop.equals(other.stop))
				return false;
			return true;
		}

		@Override
		public String toString() {
			return "StopKey [stop=" + stop + ", date=" + date + "]";
		}

	}

	public static class StopValue implements WritableComparable<StopValue> {
		// the arrive time or depart time
		private IntWritable time;

		// the delay in minutes
		private FloatWritable delay;

		// is the second leg of flight
		private BooleanWritable isDest;

		public StopValue() {
			time = new IntWritable();
			delay = new FloatWritable();
			isDest = new BooleanWritable();
		}

		public StopValue(int time, float delay, boolean isDest) {
			this.time = new IntWritable(time);
			this.delay = new FloatWritable(delay);
			this.isDest = new BooleanWritable(isDest);
		}

		@Override
		public void readFields(DataInput in) throws IOException {
			time.readFields(in);
			delay.readFields(in);
			isDest.readFields(in);
		}

		@Override
		public void write(DataOutput out) throws IOException {
			time.write(out);
			delay.write(out);
			isDest.write(out);
		}

		@Override
		public int compareTo(StopValue o) {
			int cmp = this.isDest.compareTo(o.getIsDest());
			if (cmp != 0)
				return cmp;

			cmp = this.time.compareTo(o.getTime());
			if (cmp != 0)
				return cmp;

			return this.delay.compareTo(o.getDelay());
		}

		public IntWritable getTime() {
			return time;
		}

		public void setTime(IntWritable time) {
			this.time = time;
		}

		public FloatWritable getDelay() {
			return delay;
		}

		public void setDelay(FloatWritable delay) {
			this.delay = delay;
		}

		public BooleanWritable getIsDest() {
			return isDest;
		}

		public void setIsDest(BooleanWritable isDest) {
			this.isDest = isDest;
		}

		@Override
		public String toString() {
			return "StopValue [time=" + time + ", delay=" + delay + ", isDest="
					+ isDest + "]";
		}

		@Override
		public int hashCode() {
			final int prime = 31;
			int result = 1;
			result = prime * result + ((delay == null) ? 0 : delay.hashCode());
			result = prime * result
					+ ((isDest == null) ? 0 : isDest.hashCode());
			result = prime * result + ((time == null) ? 0 : time.hashCode());
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
			StopValue other = (StopValue) obj;
			if (delay == null) {
				if (other.delay != null)
					return false;
			} else if (!delay.equals(other.delay))
				return false;
			if (isDest == null) {
				if (other.isDest != null)
					return false;
			} else if (!isDest.equals(other.isDest))
				return false;
			if (time == null) {
				if (other.time != null)
					return false;
			} else if (!time.equals(other.time))
				return false;
			return true;
		}

	}

	public static class JoinMapper extends
			Mapper<Object, Text, StopKey, StopValue> {
		public void map(Object key, Text value, Context context)
				throws IOException, InterruptedException {
			CSVParser parser = new CSVParser();
			String[] entry = parser.parseLine(value.toString());
			int flightType = getFlightType(entry);
			if (flightType == 1) {
				StopKey stopKey = new StopKey(entry[DEST], entry[FLIGHT_DATE]);
				StopValue stopValue = new StopValue(
						Integer.parseInt(entry[ARR_TIME]),
						Float.parseFloat(entry[ARR_DELAY_MINUTES]), false);
				context.write(stopKey, stopValue);
			} else if (flightType == 2) {
				StopKey stopKey = new StopKey(entry[ORIGIN], entry[FLIGHT_DATE]);
				StopValue stopValue = new StopValue(
						Integer.parseInt(entry[DEP_TIME]),
						Float.parseFloat(entry[ARR_DELAY_MINUTES]), true);
				context.write(stopKey, stopValue);
			}
		}

		private int getFlightType(String[] entry) {

			float cancelled = Float.parseFloat(entry[CANCELLED]);
			float diverted = Float.parseFloat(entry[DIVERTED]);

			if (cancelled == 1.0 || diverted == 1.0) {
				return 0;
			}

			int year = Integer.parseInt(entry[YEAR]);
			int month = Integer.parseInt(entry[MONTH]);
			String origin = entry[ORIGIN];
			String dest = entry[DEST];
//			
//			if((year == 2007 && month == 12) || (year == 2008 && month == 1)){
//				if(origin.equals("ORD") && !dest.equals("JFK")){
//					return 1;
//				}
//				
//				if(!origin.equals("ORD") && dest.equals("JFK")){
//					return 2;
//				}
//			}

			if (year < 2007 || year > 2008)
				return 0;

			if (year == 2007 && month < 6)
				return 0;

			if (year == 2008 && month > 5)
				return 0;

			if (origin.equals("ORD") && !dest.equals("JFK")) {
				return 1;
			}

			if (!origin.equals("ORD") && dest.equals("JFK")) {
				return 2;
			}

			return 0;
		}

	}

	public static class JoinReducer extends
			Reducer<StopKey, StopValue, NullWritable, FloatWritable> {
		private long count = 0;

		public void reduce(StopKey key, Iterable<StopValue> values,
				Context context) throws IOException, InterruptedException {

			List<StopValue> first = new LinkedList<StopValue>();
			List<StopValue> second = new LinkedList<StopValue>();

			for (StopValue v : values) {
				if (v.getIsDest().get()) {
					StopValue value = new StopValue(v.getTime().get(), v
							.getDelay().get(), v.getIsDest().get());
					second.add(value);
				} else {
					StopValue value = new StopValue(v.getTime().get(), v
							.getDelay().get(), v.getIsDest().get());
					first.add(value);
				}
			}
			
			count += first.size() + second.size();
			System.out.println(count);

			for (StopValue src : first) {
				for (StopValue dest : second) {
					if (src.getTime().get() < dest.getTime().get()) {
						float srcDelay = src.getDelay().get();
						float destDelay = dest.getDelay().get();
						context.write(NullWritable.get(), new FloatWritable(
								srcDelay + destDelay));
					}
				}
			}
		}
	}

	public static void main(String[] args) throws Exception {
		Configuration conf = new Configuration();
		String[] otherArgs = new GenericOptionsParser(conf, args)
				.getRemainingArgs();
		if (otherArgs.length != 2) {
			System.err.println("Usage: wordcount <in> <out>");
			System.exit(2);
		}
		Job job = new Job(conf, "word count no combiner");
		job.setJarByClass(JoinMapReducer.class);
		job.setMapperClass(JoinMapper.class);

		// No Combiner
		// job.setCombinerClass(IntSumReducer.class);
		job.setReducerClass(JoinReducer.class);
		// Set number of reduce tasks
		job.setNumReduceTasks(5);

		job.setMapOutputKeyClass(StopKey.class);
		job.setMapOutputValueClass(StopValue.class);
		job.setOutputKeyClass(NullWritable.class);
		job.setOutputValueClass(FloatWritable.class);

		FileInputFormat.addInputPath(job, new Path(otherArgs[0]));
		FileOutputFormat.setOutputPath(job, new Path(otherArgs[1]));
		System.exit(job.waitForCompletion(true) ? 0 : 1);

	}

}
