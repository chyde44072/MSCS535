// Base Vehicle class// Base Vehicle class

class Vehicle {class Vehicle {

    public void forward() {    public void forward() {

        System.out.println("Vehicle moving forward");        System.out.println("Vehicle moving forward");

    }    }

        

    public void reverse() {    public void reverse() {

        System.out.println("Vehicle moving reverse");        System.out.println("Vehicle moving reverse");

    }    }

}}



// SUV class extending Vehicle// SUV class extending Vehicle

class SUV extends Vehicle {class SUV extends Vehicle {

    @Override    @Override

    public void forward() {    public void forward() {

        System.out.println("SUV moving forward with 4WD");        System.out.println("SUV moving forward with 4WD");

    }    }

        

    @Override    @Override

    public void reverse() {    public void reverse() {

        System.out.println("SUV reversing with backup camera");        System.out.println("SUV reversing with backup camera");

    }    }

}}



// SportsCar class extending Vehicle// SportsCar class extending Vehicle

class SportsCar extends Vehicle {class SportsCar extends Vehicle {

    @Override    @Override

    public void forward() {    public void forward() {

        System.out.println("SportsCar accelerating quickly");        System.out.println("SportsCar accelerating quickly");

    }    }

        

    @Override    @Override

    public void reverse() {    public void reverse() {

        System.out.println("SportsCar reversing with sport mode");        System.out.println("SportsCar reversing with sport mode");

    }    }

}}



// Hybrid class extending Vehicle// Hybrid class extending Vehicle

class Hybrid extends Vehicle {class Hybrid extends Vehicle {

    @Override    @Override

    public void forward() {    public void forward() {

        System.out.println("Hybrid moving forward using electric motor");        System.out.println("Hybrid moving forward using electric motor");

    }    }

        

    @Override    @Override

    public void reverse() {    public void reverse() {

        System.out.println("Hybrid reversing in silent mode");        System.out.println("Hybrid reversing in silent mode");

    }    }

}}



// Test class// Test class

public class VehicleTest {public class VehicleTest {

    public static void main(String[] args) {    public static void main(String[] args) {

        Vehicle suv = new SUV();        Vehicle suv = new SUV();

        Vehicle sports = new SportsCar();        Vehicle sports = new SportsCar();

        Vehicle hybrid = new Hybrid();        Vehicle hybrid = new Hybrid();

                

        suv.forward();        suv.forward();

        suv.reverse();        suv.reverse();

                

        sports.forward();        sports.forward();

        sports.reverse();        sports.reverse();

                

        hybrid.forward();        hybrid.forward();

        hybrid.reverse();        hybrid.reverse();

    }    }

}}