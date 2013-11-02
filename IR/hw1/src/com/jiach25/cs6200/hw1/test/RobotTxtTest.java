package com.jiach25.cs6200.hw1.test;

import static org.junit.Assert.*;

import org.junit.Before;
import org.junit.Test;

import com.jiach25.cs6200.hw1.Configurable;
import com.jiach25.cs6200.hw1.RobotTxt;

public class RobotTxtTest {
	
	RobotTxt robotTxt;
	RobotTxt robotTxt1;

	@Before
	public void setUp() throws Exception {
		String seed = "http://www.ccs.neu.edu";
		Configurable config = new Configurable(seed);
		robotTxt= new RobotTxt(config);
		
		Configurable config1 = new Configurable(seed,"Mozilla 5.0");
		robotTxt1= new RobotTxt(config1);
		
	}

	@Test
	public void testGetBlackList() {
		assertEquals("http://www.ccs.neu.edu/robots.txt", robotTxt.getRobotFileUrl());
	}
	
	@Test
	public void testIsPermit(){
		String url = "http://www.ccs.neu.edu/tools/checkbot/index.html";
		assertEquals(false,robotTxt.isPermit(url));
		assertEquals(false,robotTxt1.isPermit(url));
		
		String url1 = "http://www.ccs.neu.edu/tools/checkbot/";
		assertEquals(false,robotTxt.isPermit(url1));
		assertEquals(false,robotTxt1.isPermit(url1));
		
		String url2 = "http://www.ccs.neu.edu/tools/checkbot";
		assertEquals(false,robotTxt.isPermit(url2));
		assertEquals(false,robotTxt1.isPermit(url2));
		
		String url3 = "http://www.ccs.neu.edu/tools";
		assertEquals(true,robotTxt.isPermit(url3));
		assertEquals(true,robotTxt1.isPermit(url3));
		
		String url4 = "http://www.ccs.neu.edu/home/sxhan/com1105/";
		assertEquals(true,robotTxt.isPermit(url4));
		assertEquals(false,robotTxt1.isPermit(url4));
	}

}
