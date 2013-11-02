import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Arrays;
import java.util.LinkedList;
import java.util.List;
import java.util.Scanner;

import weka.classifiers.Classifier;
import weka.classifiers.bayes.NaiveBayes;
import weka.classifiers.trees.J48;
import weka.classifiers.trees.J48graft;
import weka.core.Attribute;
import weka.core.FastVector;
import weka.core.Instance;
import weka.core.Instances;
import weka.filters.Filter;

/*
 * Using J48 classification tree with filters:
 * Filter 1: replaced missing value by mean
 * FIlter 2: remove missclassified instances.
 */
public class DMMainV2 {

	private Instances train;
	private Instances test;

	public static final int ATTR = 15;

	public DMMainV2(String trainPath, String testPath) throws Exception {
		List<String[]> raws = this.parseFile(trainPath);
		List<String[]> testRaws = this.parseFile(testPath);
		train = createInstances("train", raws, false);
		train.setClassIndex(train.numAttributes() - 1);
		preprocess();

		test = createInstances("test", testRaws, true);

		String[] classLabelList = { "<=50K", ">50K" };
		Attribute classLabel = createAttribute("classLabel", classLabelList);
		test.insertAttributeAt(classLabel, test.numAttributes());
		test.setClassIndex(test.numAttributes() - 1);

		log(train.numInstances());
		log(test.numInstances());
	}

	public void preprocess() throws Exception {

		weka.filters.unsupervised.attribute.ReplaceMissingValues scheme = new weka.filters.unsupervised.attribute.ReplaceMissingValues();
		scheme.setOptions(weka.core.Utils.splitOptions(""));
		scheme.setInputFormat(train);
		train = Filter.useFilter(train, scheme);

		weka.filters.unsupervised.instance.RemoveMisclassified scheme1 = new weka.filters.unsupervised.instance.RemoveMisclassified();
		scheme1.setOptions(weka.core.Utils
				.splitOptions("-W \"weka.classifiers.trees.J48 -C 0.25 -M 2\" -C -1 -F 0 -T 0.1 -I 0"));
		scheme1.setInputFormat(train);
		train = Filter.useFilter(train, scheme1);
	}

	public List<String[]> parseFile(String path) throws Exception {
		Scanner scan = new Scanner(new File(path));
		List<String[]> rawList = new LinkedList<String[]>();

		while (scan.hasNextLine()) {
			String line = scan.nextLine();
			String[] attributes = line.split("\t");
			rawList.add(attributes);
		}
		return rawList;
	}

	public FastVector createAttributs(boolean isTest) {

		Attribute age = createAttribute("age");

		String[] workClassList = { "Private", "Self-emp-not-inc",
				"Self-emp-inc", "Federal-gov", "Local-gov", "State-gov",
				"Without-pay", "Never-worked" };
		Attribute workClass = createAttribute("workClass", workClassList);

		Attribute fnlwgt = createAttribute("fnlwgt");

		String[] educationList = { "Bachelors", "Some-college", "11th",
				"HS-grad", "Prof-school", "Assoc-acdm", "Assoc-voc", "9th",
				"7th-8th", "12th", "Masters", "1st-4th", "10th", "Doctorate",
				"5th-6th", "Preschool" };
		Attribute education = createAttribute("education", educationList);

		Attribute educationNum = createAttribute("educationNum");

		String[] maritalStatusList = { "Married-civ-spouse", "Divorced",
				"Never-married", "Separated", "Widowed",
				"Married-spouse-absent", "Married-AF-spouse" };
		Attribute maritalStatus = createAttribute("maritalStatus",
				maritalStatusList);

		String[] occupationList = { "Tech-support", "Craft-repair",
				"Other-service", "Sales", "Exec-managerial", "Prof-specialty",
				"Handlers-cleaners", "Machine-op-inspct", "Adm-clerical",
				"Farming-fishing", "Transport-moving", "Priv-house-serv",
				"Protective-serv", "Armed-Forces" };
		Attribute occupation = createAttribute("occupation", occupationList);

		String[] relationshipList = { "Wife", "Own-child", "Husband",
				"Not-in-family", "Other-relative", "Unmarried" };
		Attribute relationship = createAttribute("relationship",
				relationshipList);

		String[] raceList = { "White", "Asian-Pac-Islander",
				"Amer-Indian-Eskimo", "Other", "Black" };
		Attribute race = createAttribute("race", raceList);

		String[] sexList = { "Female", "Male" };
		Attribute sex = createAttribute("sex", sexList);

		Attribute capitalGain = createAttribute("capitalGain");
		Attribute capitalLoss = createAttribute("capitalLoss");
		Attribute hoursPerWeek = createAttribute("hoursPerWeek");

		String[] nativeCountryList = { "United-States", "Cambodia", "England",
				"Puerto-Rico", "Canada", "Germany",
				"Outlying-US(Guam-USVI-etc)", "India", "Japan", "Greece",
				"South", "China", "Cuba", "Iran", "Honduras", "Philippines",
				"Italy", "Poland", "Jamaica", "Vietnam", "Mexico", "Portugal",
				"Ireland", "France", "Dominican-Republic", "Laos", "Ecuador",
				"Taiwan", "Haiti", "Columbia", "Hungary", "Guatemala",
				"Nicaragua", "Scotland", "Thailand", "Yugoslavia",
				"El-Salvador", "Trinadad&Tobago", "Peru", "Hong",
				"Holand-Netherlands" };
		Attribute nativeCountry = createAttribute("nativeCountry",
				nativeCountryList);

		String[] classLabelList = { "<=50K", ">50K" };
		Attribute classLabel = createAttribute("classLabel", classLabelList);

		FastVector attributes = new FastVector(ATTR);

		attributes.addElement(age);
		attributes.addElement(workClass);
		attributes.addElement(fnlwgt);
		attributes.addElement(education);

		attributes.addElement(educationNum);
		attributes.addElement(maritalStatus);
		attributes.addElement(occupation);
		attributes.addElement(relationship);

		attributes.addElement(race);
		attributes.addElement(sex);
		attributes.addElement(capitalGain);
		attributes.addElement(capitalLoss);

		attributes.addElement(hoursPerWeek);
		attributes.addElement(nativeCountry);
		if (!isTest)
			attributes.addElement(classLabel);

		return attributes;
	}

	public Attribute createAttribute(String name) {
		return new Attribute(name);
	}

	public Attribute createAttribute(String name, String[] values) {
		if (values.length == 0)
			createAttribute(name);

		FastVector list = new FastVector(values.length);
		for (String s : values)
			list.addElement(s);
		return new Attribute(name, list);
	}

	public Instances createInstances(String name, List<String[]> raws,
			boolean isTest) {
		FastVector attributes = createAttributs(isTest);
		Instances instances = new Instances(name, attributes, raws.size());

		for (String[] raw : raws) {
			Instance i = new Instance(attributes.size());
			int count = 0;

			// i.setValue((Attribute)attributes.elementAt(1),
			// Double.parseDouble(raw[0].trim()));
			try {
				while (count < attributes.size()) {
					if (raw[count].trim().equals("?") || count >= raw.length) {
						count++;
						continue;
					}

					if (isNumber(raw[count]))
						i.setValue((Attribute) attributes.elementAt(count),
								Double.parseDouble(raw[count].trim()));
					else
						i.setValue((Attribute) attributes.elementAt(count),
								raw[count].trim());
					count++;
				}
			} catch (Exception e) {
				e.printStackTrace();
				// log(count);
				// log(i);
			}
			instances.add(i);
		}
		return instances;
	}

	public boolean isNumber(String value) {
		try {
			Double.parseDouble(value);
			return true;
		} catch (Exception e) {
			return false;
		}
	}

	public Classifier classify() throws Exception {
		Classifier cModel = (Classifier) new J48();
		cModel.setOptions(weka.core.Utils.splitOptions("-C 0.25 -M 2"));
		cModel.buildClassifier(train);
		return cModel;
	}

	public void predict(Classifier cf, String output) throws Exception {
		StringBuilder sb = new StringBuilder();
		//sb.append("Category\n");
		for (int i = 0; i < test.numInstances(); i++) {
			double pred = cf.classifyInstance(test.instance(i));
			sb.append(test.classAttribute().value((int) pred));
			sb.append("\n");
		}
		saveFile(output, sb);
	}

	public void saveFile(String path, StringBuilder contents)
			throws IOException {
		BufferedWriter output = new BufferedWriter(new FileWriter(path));
		// System.out.println(contents.toString());
		output.write(contents.toString().trim());
		output.close();
	}

	public void log(Object msg) {
		//System.out.println(msg);
	}

	/**
	 * @param args
	 * @throws Exception
	 */
	public static void main(String[] args) throws Exception {
		// TODO Auto-generated method stub
		
		if(args.length!=2){
			throw new Exception("Wrong input argument!");
		}
		
		String testPath = args[0];
		String outputPath = args[1];
		
		DMMainV2 runner = new DMMainV2("training.txt", testPath);
		Classifier cf = runner.classify();
		runner.predict(cf, outputPath);
	}

}
