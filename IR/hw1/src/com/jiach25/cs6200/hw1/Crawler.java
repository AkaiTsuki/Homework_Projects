package com.jiach25.cs6200.hw1;

import java.net.HttpURLConnection;
import java.net.URL;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

public class Crawler {

	/**
	 *  Configuration of the crawler
	 */
	private Configurable config;
	
	/**
	 *  Frontier that save visited url and decide which to crawl next
	 */
	private Frontier frontier;
	
	/**
	 *  RobotTxt parses and saves the robots.txt information
	 */
	private RobotTxt robotTxt;

	public Crawler(String seed) {
		try {
			config = new Configurable(seed);
			robotTxt = new RobotTxt(config);
			frontier = new Frontier(config);
		} catch (Exception e) {
			System.out.println("Error:"+e.getMessage());
		}
	}
	
	public Crawler(String seed,String agent){
		try {
			config = new Configurable(seed,agent);
			robotTxt = new RobotTxt(config);
			frontier = new Frontier(config);
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	

	/**
	 * Crawl the website started from the seed
	 */
	public void crawl() {
		while (frontier.hasMore() && !frontier.isFinished()) {
			String url = frontier.nextUrl();

			if (!robotTxt.isPermit(url) || frontier.isVisited(url) || !this.underCurrentWebsite(url))
				continue;

			String format = this.getContentType(url);
			if (format == null || !this.isLegalFormat(format))
				continue;

			if (format.equals("application/pdf")) {
				frontier.addToVisited(url);
				continue;
			}

			Document doc;
			try {
				doc = Jsoup.connect(url).userAgent(config.getUserAgent()).get();
				Elements links = doc.select("a[href]");
				for (Element link : links) {
					String nextUrl = link.attr("abs:href");
					frontier.addToQueue(nextUrl);
				}
				frontier.addToVisited(url);
				Thread.sleep(config.getDelay());
			} catch (Exception e) {
				System.out.println("IGNORED: "+url+":"+e.getMessage());
			}

		}
	}

	/**
	 * @param format
	 * @return whether the contentType of a url is allowed to be crawled.
	 */
	private boolean isLegalFormat(String format) {
		return config.getFormat().contains(format);
	}
	
	/**
	 * @param url
	 * @return whether the given url is under current website
	 */
	private boolean underCurrentWebsite(String url){
		String domain = config.getTopDomain();
		return url.startsWith(domain);
	}

	/**
	 * @param url
	 * @return content type of given url
	 * Get the contentType in HTTP HEAD.
	 */
	private String getContentType(String url) {

		try {
			URL toTest = new URL(url);
			HttpURLConnection conn = (HttpURLConnection) toTest
					.openConnection();
			conn.setRequestMethod("HEAD");
			conn.connect();
			String contentType = conn.getContentType();
			if(contentType==null)
				return null;
			String format = contentType.split(";")[0];
			conn.disconnect();
			return format;
		} catch (Exception e) {
			System.out.println("IGNORED: "+url+":"+e.getMessage());
		}
		return null;
	}

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		try {
			
			if(args.length==2){
				String seed = args[0];
				String agent = args[1];
				Crawler c = new Crawler(seed,agent);
				c.crawl();
			}else if(args.length==1){
				String seed = args[0];
				Crawler c = new Crawler(seed);
				c.crawl();
			}else{
				System.out.println("Wrong Command! Please input in following format:");
				System.out.println("java -jar hw1.jar [seed] [user-agent(option)]");
			}		
			
		} catch (Exception e) {
			System.out.println("Error:"+e.getMessage());
		}

	}

}
