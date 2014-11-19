import dkmeans.kmeans.KMeansController;

public class Main {

    public static void main(String[] args) throws Exception {
        KMeansController controller = new KMeansController();
        controller.train(args);
    }
}
