package sorting;

import java.util.Arrays;

public class SortingMain {
	private static Class<Sort> []SORT_CLASSES = new Class [] {InsertionSort.class, BubbleSort.class, MergeSort.class};

	public static void main(String[] args) throws IllegalAccessException, InstantiationException {
		for(Class<Sort> sortClass : SORT_CLASSES) {
			System.out.println("Sorting Class: " + sortClass.getName());
			testSorting(sortClass);
		}
	}
	
	private static void testSorting(Class<Sort> sortClass) throws IllegalAccessException, InstantiationException {
		Sort sortInstance = sortClass.newInstance();
		
		print(sortInstance.sort(new Integer[]{1,3,6,5,4,8,9}));
		print(sortInstance.sort(new Integer[]{1}));
		print(sortInstance.sort(new Integer[]{}));
		print(sortInstance.sort(new Integer[]{1,1}));
		print(sortInstance.sort(new Integer[]{3,3,5,9,8,1,1}));
	}
	
	private static void print(Integer []elements) {
		System.out.println("\t" + Arrays.toString(elements));
	}

}
