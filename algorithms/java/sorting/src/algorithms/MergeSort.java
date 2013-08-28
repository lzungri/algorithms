package algorithms;

public class MergeSort implements Sort {

	public Integer[] sort(Integer[] elements) {
		if(elements.length <= 1) {
			return elements;
		}
		
		Integer []leftElements = new Integer[elements.length / 2];
		Integer []rightElements = new Integer[elements.length - elements.length / 2];
		
		System.arraycopy(elements, 0, leftElements, 0, elements.length / 2);
		System.arraycopy(elements, elements.length / 2, rightElements, 0, elements.length - elements.length / 2);
		
//		for(int i = 0; i < elements.length; ++i) {
//			if(i < elements.length / 2) {
//				leftElements[i] = elements[i];
//			} else {
//				rightElements[i - elements.length / 2] = elements[i];
//			}
//		}
		
		Integer[] left = sort(leftElements);
		Integer[] right = sort(rightElements);
		
		int i = 0;
		int j = 0;
		
		Integer[] merged = new Integer[elements.length];
		for(int index = 0; index < elements.length; ++index) {
			if(j >= right.length || (i < left.length && left[i] <= right[j])) {
				merged[index] = left[i];
				i++;
			} else {
				merged[index] = right[j];
				j++;
			}
			
		}
		return merged;
	}
	

}
