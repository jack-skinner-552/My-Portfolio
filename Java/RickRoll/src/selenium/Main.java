package selenium;

import java.time.Duration;
import java.util.concurrent.TimeUnit;

import org.openqa.selenium.By;
import org.openqa.selenium.Keys;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;

public class Main {
    public static void main(String[] args) {
        System.setProperty("webdriver.chrome.driver", "/Users/Jack/Downloads/Driver/chromedriver.exe");
        ChromeOptions options = new ChromeOptions();
        options.addArguments("--user-data-dir=C:/Users/Jack/AppData/Local/Google/Chrome/User Data/");
        options.addArguments("--profile-directory=Profile 1");

        WebDriver driver = new ChromeDriver(options);
        driver.get("https://www.youtube.com");

        // Search "Never Gonna Give You Up
        WebElement YoutubeSearch = driver.findElement(By.name("search_query"));
        YoutubeSearch.click();
        YoutubeSearch.sendKeys("Never Gonna Give You Up");
        YoutubeSearch.sendKeys(Keys.RETURN);


        // Wait 3 seconds
        try {
            TimeUnit.SECONDS.sleep(3);
        } catch (InterruptedException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }

        // Click on Correct Video
        WebElement Rick = driver.findElement(By.xpath("//*[@title='Rick Astley - Never Gonna Give You Up (Official Music Video)']"));
        Rick.click();


        // Print "You just got Rick Rolled"
        System.out.println("You just got Rick Rolled.");

        try {
            TimeUnit.SECONDS.sleep(70);
        } catch (InterruptedException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
        driver.quit();
    }
}