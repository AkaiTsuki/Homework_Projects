package com.jiach25.cs6200.hw1;

import java.util.LinkedList;
import java.util.List;
import java.util.Queue;

public class Frontier {
	
	/**
	 *  Configuration of the crawler
	 */
	private Configurable config;
	
	/**
	 * Queue that contains urls waiting to be crawled
	 */
	private Queue<String> workQueue;
	
	/**
	 *  List of url that already visited
	 */
	private List<String> visited;

	protected Frontier(Configurable config) {
		super();
		this.config = config;
		workQueue = new LinkedList<String>();
		visited = new LinkedList<String>();
		workQueue.add(config.getSeed());
	}
	
	/**
	 * @return the next URL to be retrieved.
	 * @return null if no more url in work queue.
	 */
	public String nextUrl() {
		return workQueue.poll();
	}
	
	/**
	 * @param url
	 * Add a url to visited list
	 */
	public void addToVisited(String url){
		visited.add(url);
		System.out.println(url);
	}
	
	/**
	 * @param url
	 * Add a url to work queue so that it can be visited later
	 */
	public void addToQueue(String url){
		workQueue.add(url);
	}
	
	/**
	 * @return whether the number of visited url is equal to the maximum number of url we need to retrieve
	 */
	public boolean isFinished(){
		return visited.size()>=config.getMaxUrl();
	}

	/**
	 * @return whether there is more url to retrieve
	 */
	public boolean hasMore() {
		return !(workQueue.size() == 0);
	}

	/**
	 * @param url
	 * @return whether the given url is already visited before
	 */
	public boolean isVisited(String url) {
		
		String toTest  = url;
		if(toTest.endsWith("#")){
			toTest = toTest.substring(0, toTest.length()-1);
		}
		
		for(String s: visited){
			if(s.equals(toTest))
				return true;
		}
		
		return false;
	}
	

	/**
	 * @return the config
	 */
	public Configurable getConfig() {
		return config;
	}

	/**
	 * @param config the config to set
	 */
	public void setConfig(Configurable config) {
		this.config = config;
	}

	/**
	 * @return the workQueue
	 */
	public Queue<String> getWorkQueue() {
		return workQueue;
	}

	/**
	 * @param workQueue the workQueue to set
	 */
	public void setWorkQueue(Queue<String> workQueue) {
		this.workQueue = workQueue;
	}

	/**
	 * @return the visited
	 */
	public List<String> getVisited() {
		return visited;
	}

	/**
	 * @param visited the visited to set
	 */
	public void setVisited(List<String> visited) {
		this.visited = visited;
	}

	
}
