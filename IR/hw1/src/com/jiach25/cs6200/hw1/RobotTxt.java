package com.jiach25.cs6200.hw1;

import java.io.IOException;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLConnection;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Scanner;


/**
 * @author jiachiliu
 *
 */
public class RobotTxt {
	
	private Configurable config;
	private String robotFileName = "robots.txt";
	private Map<String,List<String>> blackList;
	
	
	public RobotTxt(Configurable config) throws Exception{
		this.config = config;
		blackList = new HashMap<String,List<String>>();
		loadRobotFile(getRobotFileUrl());
	}
	
	/**
	 * @return the url of robots.txt file based on seed
	 */
	public String getRobotFileUrl(){
		return config.getTopDomain()+"/"+robotFileName;
	}
	
	/**
	 * @param robotUrl
	 * Load the robot file from target website and parse the robot file
	 * @throws Exception 
	 */
	protected void loadRobotFile(String robotUrl) throws Exception{
		try {
			URL url=new URL(robotUrl);
			URLConnection conn = url.openConnection();
			conn.setRequestProperty("User-Agent", config.getUserAgent());
			Scanner s = new Scanner(conn.getInputStream());
			
			parse(s);
			
			s.close();
		} catch (MalformedURLException e) {
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
	}
	
	/**
	 * @param s
	 * @throws Exception
	 * Scan the robots.txt file retrieved from web and construct a black list for different user agents.
	 */
	protected void parse(Scanner s) throws Exception{

		String currentAgent="";
		
		while(s.hasNextLine()){
			String line = s.nextLine();
			if(line.startsWith("User-agent:")){				
				String userAgent = line.split(":")[1].trim();
				currentAgent=userAgent;
				this.blackList.put(userAgent, new LinkedList<String>());
			}else if(line.startsWith("Disallow:")){
				List<String> list = this.blackList.get(currentAgent);
				if(list==null)
					throw new Exception("Robots.txt parse failed!");
				else
					list.add(config.getTopDomain()+line.split(":")[1].trim());
			}
		}
	}
	
	/**
	 * @param url
	 * @return whether the given url is allowed to crawl under current user-agent
	 */
	public boolean isPermit(String url){
		String toTest = url;
		if(!toTest.endsWith("/"))
			toTest+="/";
		
		List<String> list = this.blackList.get(config.getUserAgent());
		
		if(list==null)
			list = this.blackList.get("*");
		
		for(String s : list){
			if(s.equals("/"))
				return false;
			
			if(toTest.startsWith(s))
				return false;
		}
		return true;
	}

	/**
	 * @return the blackList
	 */
	public Map<String, List<String>> getBlackList() {
		return blackList;
	}

	/**
	 * @param blackList the blackList to set
	 */
	public void setBlackList(Map<String, List<String>> blackList) {
		this.blackList = blackList;
	}
	
	

}
