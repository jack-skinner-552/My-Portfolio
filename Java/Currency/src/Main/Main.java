package Main;
import java.util.*;

public class Main {
    private static double convertCurrency(double num, String o){
        double conversion = 0;
        if (o.contains("EUR")){
            conversion = num*Currencies.EUR;
        }
        else if(o.contains("GBP")){
            conversion = num*Currencies.GBP;
        }
        else if(o.contains("CAD")){
            conversion = num*Currencies.CAD;
        }
        else if(o.contains("MNT")){
            conversion = num*Currencies.MNT;
        }
        else{
            System.out.println("Invalid Currency Entered.");
            System.exit(0);
        }
        return conversion;

    }

    public static void main(String[] args) {

        Scanner input = new Scanner(System.in);

        System.out.println("Enter your dollar amount: ");
        double currencyInNum = input.nextDouble();

        System.out.println("Enter the currency type you want to convert to: ");
        String currencyOutType = input.next();

        double currencyOutNum = convertCurrency(currencyInNum, currencyOutType);

        System.out.println("Your new currency is " + currencyOutNum + " " + currencyOutType);


    }
}