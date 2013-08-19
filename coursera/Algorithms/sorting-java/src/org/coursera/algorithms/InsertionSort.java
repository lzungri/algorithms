package org.coursera.algorithms;


public class InsertionSort implements Sort {

	public Integer[] sort(Integer []elements) {
		for(int indexToSort = 1; indexToSort < elements.length; ++indexToSort) {
			Integer valueToSort = elements[indexToSort];
			
			int currentIndex = indexToSort - 1;
			while(currentIndex >= 0 && elements[currentIndex] > valueToSort ) {
				elements[currentIndex + 1] = elements[currentIndex];
				currentIndex--;
			}
			
			elements[currentIndex + 1] = valueToSort;
		}
		
		return elements;
	}
	
}
