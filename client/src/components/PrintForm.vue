<template>
  <!-- Print form will allow a member to submit a gcode file with
  print name, filament colour, printer?, weight, and duration.
  this request should be sumbitted to the DB and populated in
  PendingPrints component.
  -->
  <div>
    <h1> Print Form</h1>
    <form>
      <label for="printName">Print Name:</label><input type="text" id="printName" name="printName">
      <br />
      <label for="filColour">Filament Colour:</label><select><option>FilamentList</option></select>
      <br />
      <label for="printerType">3D Printer:</label><select><option>PrinterList</option></select>
      <br />
      <label for="printWeight">Print Weight (grams):</label><input type="text" id="printWeight" name="printWeight">
      <label for="printDuration">Print Duration:</label><input type="text" id="printDuration" name="printDuration">      
    </form>
  </div>
</template>

<script>
export default {
  name: 'PrintForm',

}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
