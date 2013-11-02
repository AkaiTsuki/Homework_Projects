package com.jiach25.cs6200.hw1;

public class Configurable {
	/**
	 * Maximum number of url to be crawled
	 */
	private int maxUrl = 100;
	
	/**
	 * User-Agent
	 */
	private String userAgent = "htdig";
	
	/**
	 * Start url
	 */
	private String seed;
	
	/**
	 * ContentType that allowed to be crawled
	 */
	private String format="text/html,application/pdf";
	
	/**
	 * Time delay between each request
	 */
	private int delay = 5000;

	public Configurable(String seed) throws Exception {
		if (!seed.startsWith("http:") && !seed.startsWith("https:"))
			throw new Exception("Unable to recognize the protocol.");

		if (seed.endsWith("/"))
			this.seed = seed.substring(0, seed.length() - 1);
		else
			this.seed = seed;
	}

	public Configurable(String seed, String userAgent) throws Exception {
		this(seed);
		this.userAgent = userAgent;
	}

	public Configurable(String seed, String userAgent, int maxUrl)
			throws Exception {
		this(seed);
		this.maxUrl = maxUrl;
		this.userAgent = userAgent;
	}

	/**
	 * @return the maxUrl
	 */
	public int getMaxUrl() {
		return maxUrl;
	}

	/**
	 * @param maxUrl
	 *            the maxUrl to set
	 */
	public void setMaxUrl(int maxUrl) {
		this.maxUrl = maxUrl;
	}

	/**
	 * @return the userAgent
	 */
	public String getUserAgent() {
		return userAgent;
	}

	/**
	 * @param userAgent
	 *            the userAgent to set
	 */
	public void setUserAgent(String userAgent) {
		this.userAgent = userAgent;
	}

	/**
	 * @return the seed
	 */
	public String getSeed() {
		return seed;
	}

	/**
	 * @param seed
	 *            the seed to set
	 */
	public void setSeed(String seed) {
		this.seed = seed;
	}

	/**
	 * @return the format
	 */
	public String getFormat() {
		return format;
	}

	/**
	 * @param format the format to set
	 */
	public void setFormat(String format) {
		this.format = format;
	}
	
	/**
	 * @return the delay
	 */
	public int getDelay() {
		return delay;
	}

	/**
	 * @param delay the delay to set
	 */
	public void setDelay(int delay) {
		this.delay = delay;
	}

	/**
	 * @return the root url of the seed
	 */
	public String getTopDomain(){
		String[] urlParts = getSeed().split("//");
		String domainParts = urlParts[1].split("/")[0];
		return urlParts[0]+"//"+domainParts;
	}

}
