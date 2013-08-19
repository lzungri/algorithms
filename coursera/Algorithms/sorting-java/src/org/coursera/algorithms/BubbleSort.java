package org.coursera.algorithms;

public class BubbleSort implements Sort {

	public Integer[] sort(Integer[] elements) {
		for(int i = 0; i < elements.length - 1; ++i) {
			for(int j = 0; j < elements.length - i - 1; ++j) {
				Integer jValue = elements[j];
				Integer nextjValue = elements[j+1];
				if(jValue > nextjValue) {
					elements[j] = nextjValue;
					elements[j+1] = jValue;
				}
			}
		}
		
		return elements;
	}

}
